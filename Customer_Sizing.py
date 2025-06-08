import streamlit as st
import pandas as pd
#import datetime
from datetime import datetime, date, timedelta  # Import specific classes
import json
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

from snowflake.snowpark.context import get_active_session

# Set page configuration
st.set_page_config(
    page_title="Snowflake Customer Sizing Tool",
    page_icon="❄️",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #29B5E8;
        text-align: center;
        margin-bottom: 1rem;
    }
    .section-header {
        font-size: 1.5rem;
        color: #29B5E8;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
        background-color: #f0f8ff;
        padding: 0.5rem;
        border-radius: 5px;
    }
    .category-label {
        font-weight: bold;
        color: #0066cc;
    }
    .stButton>button {
        background-color: #29B5E8;
        color: white;
    }
    .summary-box {
        background-color: #f0f8ff;
        padding: 1rem;
        border-radius: 5px;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)


# App title and introduction
def read_svg(path):

            with open(path, 'r') as f:

                svg_string = f.read()

            return svg_string
    
svg_content = read_svg("Snowflake_Logo.svg")
st.sidebar.image(svg_content, width=200)

def calculate_consumption_estimates():
    """
    Calculate detailed storage and compute estimates based on collected data
    Returns storage estimates, compute estimates, and monthly projections
    """

    # Storage Calculations
    initial_storage = float(st.session_state.form_data.get('initial_raw_volume', 0))
    final_storage = float(st.session_state.form_data.get('final_raw_volume', 0))

    # Storage factors
    compression_factor = 0.4  # 80% compression typical
    time_travel_factor = 1.2  # Time Travel overhead
    fail_safe_factor = 1.1    # Fail-safe overhead
    cloning_factor = 1.15     # Dev/Test clones

    total_storage_factor = compression_factor * time_travel_factor * fail_safe_factor * cloning_factor

    # Calculate effective storage
    initial_effective_storage = initial_storage * total_storage_factor
    final_effective_storage = final_storage * total_storage_factor

    # Monthly storage projections with different growth curves
    ramp_curve = st.session_state.form_data.get('ramp_up_curve', 'Moderate')
    months = list(range(1, 13))

    # Apply growth curve
    if ramp_curve == "Very Slow":
        growth_multipliers = [0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    elif ramp_curve == "Slow":
        growth_multipliers = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0]
    elif ramp_curve == "Moderate":
        growth_multipliers = [0.3, 0.4, 0.5, 0.6, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 0.98, 1.0]
    elif ramp_curve == "Fast":
        growth_multipliers = [0.4, 0.6, 0.7, 0.8, 0.85, 0.9, 0.93, 0.96, 0.98, 0.99, 1.0, 1.0]
    else:  # Very Fast
        growth_multipliers = [0.6, 0.8, 0.9, 0.95, 0.98, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]

    storage_by_month = []
    for i, multiplier in enumerate(growth_multipliers):
        monthly_storage = initial_effective_storage + (final_effective_storage - initial_effective_storage) * multiplier
        storage_by_month.append(monthly_storage)

    # Compute Calculations
    compute_estimates = []

    # ETL/ELT Compute
    pipeline_count = int(st.session_state.form_data.get('pipeline_count', 0))
    for i in range(pipeline_count):
        pipeline_name = st.session_state.form_data.get(f'pipeline_{i}_name', f'Pipeline {i+1}')
        runtime_minutes = int(st.session_state.form_data.get(f'pipeline_{i}_runtime', 30))
        jobs_per_day = int(st.session_state.form_data.get(f'pipeline_{i}_jobs_per_day', 24))
        days_per_month = int(st.session_state.form_data.get(f'pipeline_{i}_days_per_month', 22))
        concurrent_jobs = int(st.session_state.form_data.get(f'pipeline_{i}_concurrent_jobs', 5))
        volume_per_job = float(st.session_state.form_data.get(f'pipeline_{i}_volume_per_job', 10.0))

        # Determine warehouse size based on workload
        workload_intensity = volume_per_job * concurrent_jobs
        if workload_intensity < 50:
            warehouse_size, credits_per_hour = "X-Small", 1
        elif workload_intensity < 200:
            warehouse_size, credits_per_hour = "Small", 2
        elif workload_intensity < 500:
            warehouse_size, credits_per_hour = "Medium", 4
        elif workload_intensity < 1000:
            warehouse_size, credits_per_hour = "Large", 8
        else:
            warehouse_size, credits_per_hour = "X-Large", 16

        # Calculate monthly credits
        total_runtime_hours = (runtime_minutes / 60) * jobs_per_day * days_per_month
        monthly_credits = total_runtime_hours * credits_per_hour

        # Apply multi-cluster if needed
        multi_cluster = concurrent_jobs > 5
        if multi_cluster:
            cluster_count = min(10, max(2, concurrent_jobs // 3))
            monthly_credits *= (cluster_count * 0.7)  # Efficiency factor for multi-cluster
        else:
            cluster_count = 1

        compute_estimates.append({
            'name': pipeline_name,
            'type': 'ETL/ELT',
            'warehouse_size': warehouse_size,
            'credits_per_hour': credits_per_hour,
            'monthly_credits': monthly_credits,
            'cluster_count': cluster_count,
            'multi_cluster': multi_cluster
        })

    # Analytics Compute
    analytics_count = int(st.session_state.form_data.get('analytics_workload_count', 0))
    for i in range(analytics_count):
        analytics_name = st.session_state.form_data.get(f'analytics_{i}_name', f'Analytics {i+1}')
        hours_per_day = int(st.session_state.form_data.get(f'analytics_{i}_hours_per_day', 8))
        days_per_month = int(st.session_state.form_data.get(f'analytics_{i}_days_per_month', 22))
        concurrent_queries = int(st.session_state.form_data.get(f'analytics_{i}_concurrent_queries', 20))
        power_users_pct = int(st.session_state.form_data.get(f'analytics_{i}_power_users', 10))
        caching_pct = int(st.session_state.form_data.get(f'analytics_{i}_caching', 50))

        # Determine warehouse size
        complexity_factor = concurrent_queries * (1 + power_users_pct/100)
        if complexity_factor < 15:
            warehouse_size, credits_per_hour = "X-Small", 1
        elif complexity_factor < 40:
            warehouse_size, credits_per_hour = "Small", 2
        elif complexity_factor < 80:
            warehouse_size, credits_per_hour = "Medium", 4
        elif complexity_factor < 150:
            warehouse_size, credits_per_hour = "Large", 8
        else:
            warehouse_size, credits_per_hour = "X-Large", 16

        # Calculate monthly credits with caching efficiency
        base_hours = hours_per_day * days_per_month
        cache_efficiency = 1 - (caching_pct / 100 * 0.3)  # 30% reduction max from caching
        effective_hours = base_hours * cache_efficiency
        monthly_credits = effective_hours * credits_per_hour

        # Multi-cluster for high concurrency
        multi_cluster = concurrent_queries > 20
        if multi_cluster:
            cluster_count = min(10, max(2, concurrent_queries // 10))
            monthly_credits *= (cluster_count * 0.8)  # Efficiency factor
        else:
            cluster_count = 1

        compute_estimates.append({
            'name': analytics_name,
            'type': 'Analytics',
            'warehouse_size': warehouse_size,
            'credits_per_hour': credits_per_hour,
            'monthly_credits': monthly_credits,
            'cluster_count': cluster_count,
            'multi_cluster': multi_cluster
        })

    # Other Workloads Compute
    if st.session_state.form_data.get('has_other_workloads', 'No') == 'Yes':
        other_count = int(st.session_state.form_data.get('other_workload_count', 0))
        for i in range(other_count):
            other_name = st.session_state.form_data.get(f'other_{i}_name', f'Other {i+1}')
            other_type = st.session_state.form_data.get(f'other_{i}_type', 'Other')
            hours_per_day = int(st.session_state.form_data.get(f'other_{i}_hours_per_day', 8))
            days_per_month = int(st.session_state.form_data.get(f'other_{i}_days_per_month', 22))
            concurrent_queries = int(st.session_state.form_data.get(f'other_{i}_concurrent_queries', 10))
            data_volume = float(st.session_state.form_data.get(f'other_{i}_data_volume', 5.0))

            # Determine warehouse size
            workload_factor = concurrent_queries * (data_volume / 10)
            if workload_factor < 10:
                warehouse_size, credits_per_hour = "X-Small", 1
            elif workload_factor < 30:
                warehouse_size, credits_per_hour = "Small", 2
            elif workload_factor < 80:
                warehouse_size, credits_per_hour = "Medium", 4
            elif workload_factor < 150:
                warehouse_size, credits_per_hour = "Large", 8
            else:
                warehouse_size, credits_per_hour = "X-Large", 16

            monthly_credits = hours_per_day * days_per_month * credits_per_hour

            multi_cluster = concurrent_queries > 15
            if multi_cluster:
                cluster_count = min(8, max(2, concurrent_queries // 8))
                monthly_credits *= (cluster_count * 0.75)
            else:
                cluster_count = 1

            compute_estimates.append({
                'name': other_name,
                'type': other_type,
                'warehouse_size': warehouse_size,
                'credits_per_hour': credits_per_hour,
                'monthly_credits': monthly_credits,
                'cluster_count': cluster_count,
                'multi_cluster': multi_cluster
            })

    # Calculate monthly compute projections
    total_base_credits = sum([est['monthly_credits'] for est in compute_estimates])
    compute_by_month = []
    for multiplier in growth_multipliers:
        monthly_compute = total_base_credits * multiplier
        compute_by_month.append(monthly_compute)

    return {
        'storage': {
            'initial': initial_effective_storage,
            'final': final_effective_storage,
            'monthly': storage_by_month,
            'compression_factor': compression_factor,
            'total_factor': total_storage_factor
        },
        'compute': {
            'estimates': compute_estimates,
            'monthly': compute_by_month,
            'total_monthly_credits': total_base_credits
        },
        'months': months,
        'growth_curve': ramp_curve
    }

def create_consumption_charts(consumption_data):
    """
    Create Streamlit charts for storage and compute consumption
    """

    # Storage Growth Chart
    st.markdown("### 📊 Storage Growth Projection")

    storage_df = pd.DataFrame({
        'Month': consumption_data['months'],
        'Storage (TB)': consumption_data['storage']['monthly']
    })

    fig_storage = px.line(storage_df, x='Month', y='Storage (TB)',
                         title=f'Projected Storage Growth - {consumption_data["growth_curve"]} Ramp-up',
                         markers=True)
    fig_storage.update_traces(line=dict(width=3))
    fig_storage.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig_storage, use_container_width=True)

    # Compute Credits Chart
    st.markdown("### 💻 Compute Credits Projection")

    compute_df = pd.DataFrame({
        'Month': consumption_data['months'],
        'Credits': consumption_data['compute']['monthly']
    })

    fig_compute = px.bar(compute_df, x='Month', y='Credits',
                        title='Projected Monthly Compute Credits',
                        color='Credits',
                        color_continuous_scale='Blues')
    fig_compute.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig_compute, use_container_width=True)

    # Warehouse Distribution Chart
    st.markdown("### 🏭 Warehouse Size Distribution")

    warehouse_df = pd.DataFrame(consumption_data['compute']['estimates'])
    size_counts = warehouse_df['warehouse_size'].value_counts()

    fig_warehouses = px.pie(values=size_counts.values, names=size_counts.index,
                           title='Distribution of Warehouse Sizes')
    fig_warehouses.update_layout(height=400)
    st.plotly_chart(fig_warehouses, use_container_width=True)

    # Credits by Workload Type
    st.markdown("### 🔄 Credits by Workload Type")

    workload_credits = warehouse_df.groupby('type')['monthly_credits'].sum().reset_index()

    fig_workload = px.bar(workload_credits, x='type', y='monthly_credits',
                         title='Monthly Credits by Workload Type',
                         color='type')
    fig_workload.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig_workload, use_container_width=True)

    return storage_df, compute_df, warehouse_df

def display_cost_estimates(consumption_data):
    """
    Display detailed cost estimates and recommendations
    """

    # Pricing assumptions (you can adjust these)
    STORAGE_COST_PER_TB = 23  # USD per TB per month
    CREDIT_COST = 3  # USD per credit (varies by region/contract)

    st.markdown("### 💰 Cost Estimates")

    # Storage costs
    final_storage_cost = consumption_data['storage']['final'] * STORAGE_COST_PER_TB

    # Compute costs
    final_compute_cost = consumption_data['compute']['total_monthly_credits'] * CREDIT_COST

    # Total cost
    total_monthly_cost = final_storage_cost + final_compute_cost
    annual_cost = total_monthly_cost * 12

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Monthly Storage Cost", f"${final_storage_cost:,.0f}")

    with col2:
        st.metric("Monthly Compute Cost", f"${final_compute_cost:,.0f}")

    with col3:
        st.metric("Total Monthly Cost", f"${total_monthly_cost:,.0f}")

    with col4:
        st.metric("Estimated Annual Cost", f"${annual_cost:,.0f}")

    # Cost breakdown chart
    cost_breakdown = pd.DataFrame({
        'Cost Type': ['Storage', 'Compute'],
        'Monthly Cost': [final_storage_cost, final_compute_cost]
    })

    fig_cost = px.pie(cost_breakdown, values='Monthly Cost', names='Cost Type',
                     title='Monthly Cost Breakdown')
    st.plotly_chart(fig_cost, use_container_width=True)

    return {
        'storage_cost': final_storage_cost,
        'compute_cost': final_compute_cost,
        'total_monthly': total_monthly_cost,
        'annual': annual_cost
    }


def write_to_snowflake():
    """
    Write all collected form data to Snowflake database
    """
    try:
        # Get active Snowflake session
        session = get_active_session()

        # # Generate a unique sizing ID
        # sizing_id = f"SIZING_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        # st.write(sizing_id)
        # Prepare main sizing record
        main_record = {
            'SIZING_ID': sizing_id,
            'CUSTOMER_NAME': st.session_state.form_data.get('customer_name', ''),
            'INDUSTRY': st.session_state.form_data.get('industry', ''),
            'CONTACT_NAME': st.session_state.form_data.get('contact_name', ''),
            'CONTACT_EMAIL': st.session_state.form_data.get('contact_email', ''),
            'COMPANY_SIZE': st.session_state.form_data.get('company_size', ''),
            'EXISTING_DATA_PLATFORM': json.dumps(st.session_state.form_data.get('existing_data_platform', [])),
            'BUSINESS_OWNER': st.session_state.form_data.get('business_owner', ''),
            'TECH_OWNER': st.session_state.form_data.get('tech_owner', ''),
            'DEV_START_DATE': str(st.session_state.form_data.get('dev_start_date', '')),
            'GO_LIVE_DATE': str(st.session_state.form_data.get('go_live_date', '')),
            'SUCCESS_METRICS': st.session_state.form_data.get('success_metrics', ''),
            'ROADBLOCKS': st.session_state.form_data.get('roadblocks', ''),
            'RAMP_UP_CURVE': st.session_state.form_data.get('ramp_up_curve', ''),
            'DATA_SOURCES_COUNT': st.session_state.form_data.get('data_sources_count', 0),
            'INITIAL_RAW_VOLUME_TB': st.session_state.form_data.get('initial_raw_volume', 0.0),
            'FINAL_RAW_VOLUME_TB': st.session_state.form_data.get('final_raw_volume', 0.0),
            'TOOLS': json.dumps(st.session_state.form_data.get('tools', [])),
            'DATA_RETENTION_PERIOD': st.session_state.form_data.get('data_retention_period', 12),
            'DATA_SENSITIVITY': st.session_state.form_data.get('data_sensitivity', ''),
            'EXPECTED_WAREHOUSES': st.session_state.form_data.get('expected_warehouses', 0),
            'TOTAL_USERS': st.session_state.form_data.get('total_users', 0),
            'QUERY_COMPLEXITY': st.session_state.form_data.get('query_complexity', ''),
            'HAS_OTHER_WORKLOADS': st.session_state.form_data.get('has_other_workloads', 'No'),
            'GEOGRAPHIC_DISTRIBUTION': json.dumps(st.session_state.form_data.get('geographic_distribution', [])),
            'HIGH_AVAILABILITY_REQUIREMENTS': st.session_state.form_data.get('high_availability_requirements', ''),
            'DISASTER_RECOVERY_REQUIREMENTS': st.session_state.form_data.get('disaster_recovery_requirements', ''),
            'CREATED_TIMESTAMP': datetime.now()
        }

        # Insert main record
        main_df = session.create_dataframe([main_record])
        #st.write(main_df)
        main_df.write.mode("append").save_as_table("SIZING_TOOL.CUSTOMER_SIZING.SIZING_MAIN")

        # Insert data sources
        data_sources_count = int(st.session_state.form_data.get('data_sources_count', 0))
        for i in range(data_sources_count):
            source_record = {
                'SIZING_ID': sizing_id,
                'SOURCE_INDEX': i + 1,
                'SOURCE_NAME': st.session_state.form_data.get(f'source_name_{i}', ''),
                'SOURCE_TYPE': st.session_state.form_data.get(f'source_type_{i}', ''),
                'CURRENT_VOLUME_TB': st.session_state.form_data.get(f'current_volume_{i}', 0.0),
                'CREATED_TIMESTAMP': datetime.now()
            }
            source_df = session.create_dataframe([source_record])
            #st.write(source_df)
            source_df.write.mode("append").save_as_table("SIZING_TOOL.CUSTOMER_SIZING.DATA_SOURCES")

        # Insert pipeline information
        pipeline_count = int(st.session_state.form_data.get('pipeline_count', 0))
        for i in range(pipeline_count):
            pipeline_record = {
                'SIZING_ID': sizing_id,
                'PIPELINE_INDEX': i + 1,
                'PIPELINE_NAME': st.session_state.form_data.get(f'pipeline_{i}_name', ''),
                'FREQUENCY': st.session_state.form_data.get(f'pipeline_{i}_frequency', ''),
                'JOBS_PER_DAY': st.session_state.form_data.get(f'pipeline_{i}_jobs_per_day', 0),
                'VOLUME_PER_JOB_GB': st.session_state.form_data.get(f'pipeline_{i}_volume_per_job', 0.0),
                'RUNTIME_MINUTES': st.session_state.form_data.get(f'pipeline_{i}_runtime', 0),
                'DAYS_PER_MONTH': st.session_state.form_data.get(f'pipeline_{i}_days_per_month', 0),
                'CONCURRENT_JOBS': st.session_state.form_data.get(f'pipeline_{i}_concurrent_jobs', 0),
                'PEAK_DURATION_MINUTES': st.session_state.form_data.get(f'pipeline_{i}_peak_duration', 0),
                'CREATED_TIMESTAMP': datetime.now()
            }
            pipeline_df = session.create_dataframe([pipeline_record])
            #st.write(pipeline_df)
            pipeline_df.write.mode("append").save_as_table("SIZING_TOOL.CUSTOMER_SIZING.PIPELINES")

        # Insert analytics workloads
        analytics_count = int(st.session_state.form_data.get('analytics_workload_count', 0))
        for i in range(analytics_count):
            analytics_record = {
                'SIZING_ID': sizing_id,
                'ANALYTICS_INDEX': i + 1,
                'WORKLOAD_NAME': st.session_state.form_data.get(f'analytics_{i}_name', ''),
                'PRIMARY_TOOL': st.session_state.form_data.get(f'analytics_{i}_tool', ''),
                'HOURS_PER_DAY': st.session_state.form_data.get(f'analytics_{i}_hours_per_day', 0),
                'DAYS_PER_MONTH': st.session_state.form_data.get(f'analytics_{i}_days_per_month', 0),
                'QUERIES_PER_DAY': st.session_state.form_data.get(f'analytics_{i}_queries_per_day', 0),
                'BASIC_USERS_PCT': st.session_state.form_data.get(f'analytics_{i}_basic_users', 0),
                'EXPERT_USERS_PCT': st.session_state.form_data.get(f'analytics_{i}_expert_users', 0),
                'POWER_USERS_PCT': st.session_state.form_data.get(f'analytics_{i}_power_users', 0),
                'PEAK_DAYS': st.session_state.form_data.get(f'analytics_{i}_peak_days', 0),
                'PEAKS_PER_DAY': st.session_state.form_data.get(f'analytics_{i}_peaks_per_day', 0),
                'PEAK_DURATION_MINUTES': st.session_state.form_data.get(f'analytics_{i}_peak_duration', 0),
                'CONCURRENT_QUERIES': st.session_state.form_data.get(f'analytics_{i}_concurrent_queries', 0),
                'CACHING_PCT': st.session_state.form_data.get(f'analytics_{i}_caching', 0),
                'CREATED_TIMESTAMP': datetime.now()
            }
            analytics_df = session.create_dataframe([analytics_record])
            #st.write(analytics_df)
            analytics_df.write.mode("append").save_as_table("SIZING_TOOL.CUSTOMER_SIZING.ANALYTICS_WORKLOADS")

        # Insert other workloads if they exist
        if st.session_state.form_data.get('has_other_workloads', 'No') == 'Yes':
            other_count = int(st.session_state.form_data.get('other_workload_count', 0))
            for i in range(other_count):
                other_record = {
                    'SIZING_ID': sizing_id,
                    'OTHER_INDEX': i + 1,
                    'WORKLOAD_NAME': st.session_state.form_data.get(f'other_{i}_name', ''),
                    'WORKLOAD_TYPE': st.session_state.form_data.get(f'other_{i}_type', ''),
                    'HOURS_PER_DAY': st.session_state.form_data.get(f'other_{i}_hours_per_day', 0),
                    'DAYS_PER_MONTH': st.session_state.form_data.get(f'other_{i}_days_per_month', 0),
                    'QUERIES_PER_DAY': st.session_state.form_data.get(f'other_{i}_queries_per_day', 0),
                    'DATA_VOLUME_GB': st.session_state.form_data.get(f'other_{i}_data_volume', 0.0),
                    'PEAK_DAYS': st.session_state.form_data.get(f'other_{i}_peak_days', 0),
                    'PEAKS_PER_DAY': st.session_state.form_data.get(f'other_{i}_peaks_per_day', 0),
                    'PEAK_DURATION_MINUTES': st.session_state.form_data.get(f'other_{i}_peak_duration', 0),
                    'CONCURRENT_QUERIES': st.session_state.form_data.get(f'other_{i}_concurrent_queries', 0),
                    'CREATED_TIMESTAMP': datetime.now()
                }
                other_df = session.create_dataframe([other_record])
                #st.write(other_df)
                other_df.write.mode("append").save_as_table("SIZING_TOOL.CUSTOMER_SIZING.OTHER_WORKLOADS")

        st.success(f"✅ Data successfully saved to Snowflake! Sizing ID: {sizing_id}")
        return sizing_id

    except Exception as e:
        st.error(f"❌ Error saving to Snowflake: {str(e)}")
        return None

st.markdown("<h1 class='main-header'>Snowflake Customer Sizing Tool</h1>", unsafe_allow_html=True)
st.markdown("""
This tool helps accurately predict storage and compute requirements for new Snowflake customers.
Please provide detailed information in each section to generate an accurate sizing estimate.
""")

# Initialize session state for storing form data
if 'form_data' not in st.session_state:
    st.session_state.form_data = {}

if 'current_section' not in st.session_state:
    st.session_state.current_section = 0

if 'show_summary' not in st.session_state:
    st.session_state.show_summary = False

# Define sections
sections = [
    "Customer Information",
    "Use Case Timeline",
    "Technical Overview",
    "Data Loading & Transformation",
    "Analytics Workload",
    "Other Workloads",
    "Summary & Recommendations"
]

# Function to navigate between sections
def next_section():
    if st.session_state.current_section < len(sections) - 1:
        st.session_state.current_section += 1
    else:
        st.session_state.show_summary = True

def prev_section():
    if st.session_state.current_section > 0:
        st.session_state.current_section -= 1

# Sidebar navigation
st.sidebar.title("Navigation")
for i, section in enumerate(sections):
    if st.sidebar.button(section, key=f"nav_{i}"):
        st.session_state.current_section = i
        if i == len(sections) - 1:
            st.session_state.show_summary = True
        else:
            st.session_state.show_summary = False

st.sidebar.markdown("---")
st.sidebar.markdown("### Progress")
progress = (st.session_state.current_section) / (len(sections) - 1)
st.sidebar.progress(progress)

# Customer Information Section
if st.session_state.current_section == 0:
    st.markdown("<h2 class='section-header'>Customer Information</h2>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.session_state.form_data['customer_name'] = st.text_input("Customer Name", 
                                                                   st.session_state.form_data.get('customer_name', ''))
        st.session_state.form_data['industry'] = st.selectbox("Industry", 
                                                             ["Retail", "Healthcare", "Financial Services", "Manufacturing", 
                                                              "Technology", "Media & Entertainment", "Other"],
                                                             index=["Retail", "Healthcare", "Financial Services", "Manufacturing", 
                                                                    "Technology", "Media & Entertainment", "Other"].index(st.session_state.form_data.get('industry', 'Retail')))

    with col2:
        st.session_state.form_data['contact_name'] = st.text_input("Primary Contact Name", 
                                                                  st.session_state.form_data.get('contact_name', ''))
        st.session_state.form_data['contact_email'] = st.text_input("Contact Email", 
                                                                   st.session_state.form_data.get('contact_email', ''))

    st.session_state.form_data['company_size'] = st.radio("Company Size", 
                                                         ["Small (< 100 employees)", "Medium (100-1000 employees)", "Large (> 1000 employees)"],
                                                         index=["Small (< 100 employees)", "Medium (100-1000 employees)", "Large (> 1000 employees)"].index(st.session_state.form_data.get('company_size', "Medium (100-1000 employees)")))

    st.session_state.form_data['existing_data_platform'] = st.multiselect("Existing Data Platform(s)", 
                                                                         ["On-premises data warehouse", "Cloud data warehouse", "Data lake", 
                                                                          "Hadoop", "None/Spreadsheets", "Other"],
                                                                         default=st.session_state.form_data.get('existing_data_platform', []))

    st.markdown("---")
    col1, col2 = st.columns([1, 1])
    with col2:
        if st.button("Next: Use Case Timeline", key="next_0"):
            next_section()

# Use Case Timeline Section
elif st.session_state.current_section == 1:
    st.markdown("<h2 class='section-header'>Use Case Timeline</h2>", unsafe_allow_html=True)

    st.markdown("<p class='category-label'>Deployment Timeline</p>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.session_state.form_data['business_owner'] = st.text_input("Business Owner", 
                                                                    st.session_state.form_data.get('business_owner', ''))

        #today = datetime.date.today()
        today = date.today()
        #default_dev_start = today + datetime.timedelta(days=30)
        #default_go_live = today + datetime.timedelta(days=90)
        default_dev_start = today + timedelta(days=30)
        default_go_live = today + timedelta(days=90)

        st.session_state.form_data['dev_start_date'] = st.date_input("Development Start Date", 
                                                                    st.session_state.form_data.get('dev_start_date', default_dev_start))

    with col2:
        st.session_state.form_data['tech_owner'] = st.text_input("Technical Owner", 
                                                                st.session_state.form_data.get('tech_owner', ''))

        st.session_state.form_data['go_live_date'] = st.date_input("Go-Live Date", 
                                                                  st.session_state.form_data.get('go_live_date', default_go_live))

    st.session_state.form_data['success_metrics'] = st.text_area("Success Metrics for this Use Case", 
                                                                st.session_state.form_data.get('success_metrics', ''))

    st.session_state.form_data['roadblocks'] = st.text_area("Potential Roadblocks or Risks", 
                                                           st.session_state.form_data.get('roadblocks', ''))

    st.session_state.form_data['ramp_up_curve'] = st.select_slider("Expected Ramp-up Curve", 
                                                                  options=["Very Slow", "Slow", "Moderate", "Fast", "Very Fast"],
                                                                  value=st.session_state.form_data.get('ramp_up_curve', "Moderate"))

    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("Previous", key="prev_1"):
            prev_section()
    with col3:
        if st.button("Next: Technical Overview", key="next_1"):
            next_section()

# Technical Overview Section
elif st.session_state.current_section == 2:
    st.markdown("<h2 class='section-header'>Technical Overview</h2>", unsafe_allow_html=True)

    st.markdown("<p class='category-label'>Database/Data Lake</p>", unsafe_allow_html=True)

    st.session_state.form_data['data_sources_count'] = st.number_input("How many relevant data sources for this use case?", 
                                                                      min_value=1, max_value=100, 
                                                                      value=int(st.session_state.form_data.get('data_sources_count', 3)))

    # Create dynamic fields for each data source
    data_sources = []
    for i in range(int(st.session_state.form_data['data_sources_count'])):
        st.markdown(f"#### Data Source {i+1}")
        col1, col2, col3 = st.columns(3)
        with col1:
            source_name = st.text_input(f"Source Name", key=f"source_name_{i}", 
                                       value=st.session_state.form_data.get(f'source_name_{i}', f'Source {i+1}'))
        with col2:
            source_type = st.selectbox(f"Source Type", 
                                      ["Relational Database", "NoSQL Database", "Files (CSV, JSON, etc.)", 
                                       "API", "Streaming", "Other"],
                                      key=f"source_type_{i}",
                                      index=["Relational Database", "NoSQL Database", "Files (CSV, JSON, etc.)", 
                                             "API", "Streaming", "Other"].index(st.session_state.form_data.get(f'source_type_{i}', "Relational Database")))
        with col3:
            current_volume = st.number_input(f"Current Raw Data Volume (TB)", 
                                           min_value=0.0, value=float(st.session_state.form_data.get(f'current_volume_{i}', 1.0)),
                                           key=f"current_volume_{i}")

        st.session_state.form_data[f'source_name_{i}'] = source_name
        st.session_state.form_data[f'source_type_{i}'] = source_type
        st.session_state.form_data[f'current_volume_{i}'] = current_volume

        data_sources.append({
            'name': source_name,
            'type': source_type,
            'volume': current_volume
        })

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        st.session_state.form_data['initial_raw_volume'] = st.number_input("Initial raw data volume expected in Snowflake (TB)", 
                                                                          min_value=0.0, 
                                                                          value=float(st.session_state.form_data.get('initial_raw_volume', 
                                                                                                                    sum([src['volume'] for src in data_sources]))))

    with col2:
        st.session_state.form_data['final_raw_volume'] = st.number_input("Final raw data volume expected after 12 months in Snowflake (TB)", 
                                                                        min_value=0.0, 
                                                                        value=float(st.session_state.form_data.get('final_raw_volume', 
                                                                                                                  st.session_state.form_data.get('initial_raw_volume', 0) * 2)))

    st.markdown("<p class='category-label'>Use Case Scope</p>", unsafe_allow_html=True)

    st.session_state.form_data['tools'] = st.multiselect("Which applications/tools will be used to load, transform and analyze this data?",
                                                        ["Snowsight", "Tableau", "Power BI", "Looker", "Qlik", 
                                                         "Informatica", "Talend", "Matillion", "Fivetran", 
                                                         "dbt", "Python", "R", "Spark", "Custom Applications", "Other"],
                                                        default=st.session_state.form_data.get('tools', ["Snowsight"]))

    # Additional questions that might be helpful
    st.markdown("### Additional Information")

    col1, col2 = st.columns(2)
    with col1:
        st.session_state.form_data['data_retention_period'] = st.slider("Data Retention Period (months)", 
                                                                       min_value=1, max_value=84, 
                                                                       value=int(st.session_state.form_data.get('data_retention_period', 12)))

    with col2:
        st.session_state.form_data['data_sensitivity'] = st.selectbox("Data Sensitivity Level",
                                                                     ["Public", "Internal", "Confidential", "Restricted"],
                                                                     index=["Public", "Internal", "Confidential", "Restricted"].index(st.session_state.form_data.get('data_sensitivity', "Internal")))

    st.session_state.form_data['expected_warehouses'] = st.number_input("Expected number of warehouses needed", 
                                                                       min_value=1, max_value=20, 
                                                                       value=int(st.session_state.form_data.get('expected_warehouses', 3)))

    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("Previous", key="prev_2"):
            prev_section()
    with col3:
        if st.button("Next: Data Loading & Transformation", key="next_2"):
            next_section()

# Data Loading & Transformation Section
elif st.session_state.current_section == 3:
    st.markdown("<h2 class='section-header'>Data Loading & Transformation</h2>", unsafe_allow_html=True)

    st.markdown("<p class='category-label'>Data Pipelines</p>", unsafe_allow_html=True)

    # Get number of ETL/ELT pipelines
    st.session_state.form_data['pipeline_count'] = st.number_input("How many distinct ETL/ELT pipelines will you have?", 
                                                                  min_value=1, max_value=20, 
                                                                  value=int(st.session_state.form_data.get('pipeline_count', 1)))

    # For each pipeline, collect details
    for i in range(int(st.session_state.form_data['pipeline_count'])):
        st.markdown(f"### Pipeline {i+1}")

        col1, col2 = st.columns(2)
        with col1:
            st.session_state.form_data[f'pipeline_{i}_name'] = st.text_input("Pipeline Name", 
                                                                            key=f"pipeline_{i}_name",
                                                                            value=st.session_state.form_data.get(f'pipeline_{i}_name', f"Pipeline {i+1}"))

            st.session_state.form_data[f'pipeline_{i}_frequency'] = st.selectbox("How often does data need to be loaded?",
                                                                                ["Real-time/Streaming", "Every few minutes", "Hourly", 
                                                                                 "Daily", "Weekly", "Monthly", "Ad-hoc"],
                                                                                key=f"pipeline_{i}_frequency",
                                                                                index=["Real-time/Streaming", "Every few minutes", "Hourly", 
                                                                                       "Daily", "Weekly", "Monthly", "Ad-hoc"].index(st.session_state.form_data.get(f'pipeline_{i}_frequency', "Daily")))

            st.session_state.form_data[f'pipeline_{i}_jobs_per_day'] = st.number_input("Average number of jobs per day", 
                                                                                      min_value=1, max_value=1000, 
                                                                                      key=f"pipeline_{i}_jobs_per_day",
                                                                                      value=int(st.session_state.form_data.get(f'pipeline_{i}_jobs_per_day', 24)))

            st.session_state.form_data[f'pipeline_{i}_volume_per_job'] = st.number_input("Average data volume processed per job (GB)", 
                                                                                        min_value=0.1, max_value=10000.0, 
                                                                                        key=f"pipeline_{i}_volume_per_job",
                                                                                        value=float(st.session_state.form_data.get(f'pipeline_{i}_volume_per_job', 10.0)))

        with col2:
            st.session_state.form_data[f'pipeline_{i}_runtime'] = st.number_input("Average run time per job (minutes)", 
                                                                                 min_value=1, max_value=1440, 
                                                                                 key=f"pipeline_{i}_runtime",
                                                                                 value=int(st.session_state.form_data.get(f'pipeline_{i}_runtime', 30)))

            st.session_state.form_data[f'pipeline_{i}_days_per_month'] = st.slider("Average number of days per month you process data", 
                                                                                  min_value=1, max_value=31, 
                                                                                  key=f"pipeline_{i}_days_per_month",
                                                                                  value=int(st.session_state.form_data.get(f'pipeline_{i}_days_per_month', 22)))

            st.session_state.form_data[f'pipeline_{i}_concurrent_jobs'] = st.number_input("Average number of jobs running concurrently at peak", 
                                                                                         min_value=1, max_value=100, 
                                                                                         key=f"pipeline_{i}_concurrent_jobs",
                                                                                         value=int(st.session_state.form_data.get(f'pipeline_{i}_concurrent_jobs', 5)))

            st.session_state.form_data[f'pipeline_{i}_peak_duration'] = st.number_input("Average duration of a peak (minutes)", 
                                                                                       min_value=1, max_value=1440, 
                                                                                       key=f"pipeline_{i}_peak_duration",
                                                                                       value=int(st.session_state.form_data.get(f'pipeline_{i}_peak_duration', 60)))

    # Additional questions
    st.markdown("### Additional Pipeline Information")

    st.session_state.form_data['data_transformation_complexity'] = st.select_slider("Data Transformation Complexity", 
                                                                                   options=["Very Simple", "Simple", "Moderate", "Complex", "Very Complex"],
                                                                                   value=st.session_state.form_data.get('data_transformation_complexity', "Moderate"))

    st.session_state.form_data['pipeline_tools'] = st.multiselect("Tools used for data pipelines",
                                                                 ["Snowflake Tasks", "Snowpipe", "Matillion", "Fivetran", 
                                                                  "Informatica", "Talend", "dbt", "Custom Scripts", "Other"],
                                                                 default=st.session_state.form_data.get('pipeline_tools', ["Snowflake Tasks"]))

    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("Previous", key="prev_3"):
            prev_section()
    with col3:
        if st.button("Next: Analytics Workload", key="next_3"):
            next_section()

# Analytics Workload Section
elif st.session_state.current_section == 4:
    st.markdown("<h2 class='section-header'>Analytics Workload</h2>", unsafe_allow_html=True)

    st.markdown("<p class='category-label'>Analytics</p>", unsafe_allow_html=True)

    # Get number of analytics workloads
    st.session_state.form_data['analytics_workload_count'] = st.number_input("How many distinct analytics workloads will you have?", 
                                                                            min_value=1, max_value=10, 
                                                                            value=int(st.session_state.form_data.get('analytics_workload_count', 1)))

    # For each analytics workload, collect details
    for i in range(int(st.session_state.form_data['analytics_workload_count'])):
        st.markdown(f"### Analytics Workload {i+1}")

        col1, col2 = st.columns(2)
        with col1:
            st.session_state.form_data[f'analytics_{i}_name'] = st.text_input("Workload Name", 
                                                                             key=f"analytics_{i}_name",
                                                                             value=st.session_state.form_data.get(f'analytics_{i}_name', f"Analytics {i+1}"))

            st.session_state.form_data[f'analytics_{i}_tool'] = st.selectbox("Primary Analytics Tool",
                                                                            ["Snowsight", "Tableau", "Power BI", "Looker", 
                                                                             "Qlik", "Excel", "Python/Jupyter", "R Studio", "Other"],
                                                                            key=f"analytics_{i}_tool",
                                                                            index=["Snowsight", "Tableau", "Power BI", "Looker", 
                                                                                   "Qlik", "Excel", "Python/Jupyter", "R Studio", "Other"].index(st.session_state.form_data.get(f'analytics_{i}_tool', "Snowsight")))

            st.session_state.form_data[f'analytics_{i}_hours_per_day'] = st.slider("Average number of hours per day users use the tool", 
                                                                                  min_value=1, max_value=24, 
                                                                                  key=f"analytics_{i}_hours_per_day",
                                                                                  value=int(st.session_state.form_data.get(f'analytics_{i}_hours_per_day', 8)))

            st.session_state.form_data[f'analytics_{i}_days_per_month'] = st.slider("Average number of days per month users use the tool", 
                                                                                   min_value=1, max_value=31, 
                                                                                   key=f"analytics_{i}_days_per_month",
                                                                                   value=int(st.session_state.form_data.get(f'analytics_{i}_days_per_month', 22)))

            st.session_state.form_data[f'analytics_{i}_queries_per_day'] = st.number_input("Average number of queries triggered per day", 
                                                                                          min_value=1, max_value=100000, 
                                                                                          key=f"analytics_{i}_queries_per_day",
                                                                                          value=int(st.session_state.form_data.get(f'analytics_{i}_queries_per_day', 1000)))

        with col2:
            # User distribution
            st.markdown("User Distribution:")
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.session_state.form_data[f'analytics_{i}_basic_users'] = st.slider("Basic Users (%)", 
                                                                                    min_value=0, max_value=100, 
                                                                                    key=f"analytics_{i}_basic_users",
                                                                                    value=int(st.session_state.form_data.get(f'analytics_{i}_basic_users', 60)))
            with col_b:
                st.session_state.form_data[f'analytics_{i}_expert_users'] = st.slider("Expert Users (%)", 
                                                                                     min_value=0, max_value=100, 
                                                                                     key=f"analytics_{i}_expert_users",
                                                                                     value=int(st.session_state.form_data.get(f'analytics_{i}_expert_users', 30)))
            with col_c:
                st.session_state.form_data[f'analytics_{i}_power_users'] = st.slider("Power Users (%)", 
                                                                                    min_value=0, max_value=100, 
                                                                                    key=f"analytics_{i}_power_users",
                                                                                    value=int(st.session_state.form_data.get(f'analytics_{i}_power_users', 10)))

            # Check if percentages add up to 100
            total = (st.session_state.form_data[f'analytics_{i}_basic_users'] + 
                     st.session_state.form_data[f'analytics_{i}_expert_users'] + 
                     st.session_state.form_data[f'analytics_{i}_power_users'])

            if total != 100:
                st.warning(f"User percentages should add up to 100%. Current total: {total}%")

            st.session_state.form_data[f'analytics_{i}_peak_days'] = st.number_input("Average number of peak days in a month", 
                                                                                    min_value=1, max_value=31, 
                                                                                    key=f"analytics_{i}_peak_days",
                                                                                    value=int(st.session_state.form_data.get(f'analytics_{i}_peak_days', 5)))

            st.session_state.form_data[f'analytics_{i}_peaks_per_day'] = st.number_input("Average number of peaks per day", 
                                                                                        min_value=1, max_value=24, 
                                                                                        key=f"analytics_{i}_peaks_per_day",
                                                                                        value=int(st.session_state.form_data.get(f'analytics_{i}_peaks_per_day', 2)))

            st.session_state.form_data[f'analytics_{i}_peak_duration'] = st.number_input("Average duration of a peak (minutes)", 
                                                                                        min_value=1, max_value=1440, 
                                                                                        key=f"analytics_{i}_peak_duration",
                                                                                        value=int(st.session_state.form_data.get(f'analytics_{i}_peak_duration', 60)))

        col1, col2 = st.columns(2)
        with col1:
            st.session_state.form_data[f'analytics_{i}_concurrent_queries'] = st.number_input("Average number of queries running concurrently at peak", 
                                                                                             min_value=1, max_value=1000, 
                                                                                             key=f"analytics_{i}_concurrent_queries",
                                                                                             value=int(st.session_state.form_data.get(f'analytics_{i}_concurrent_queries', 20)))

        with col2:
            st.session_state.form_data[f'analytics_{i}_caching'] = st.slider("Percentage of dashboards leveraging caching/in-memory structures", 
                                                                            min_value=0, max_value=100, 
                                                                            key=f"analytics_{i}_caching",
                                                                            value=int(st.session_state.form_data.get(f'analytics_{i}_caching', 50)))

    # Additional questions
    st.markdown("### Additional Analytics Information")

    st.session_state.form_data['total_users'] = st.number_input("Total number of users who will access Snowflake", 
                                                               min_value=1, max_value=10000, 
                                                               value=int(st.session_state.form_data.get('total_users', 50)))

    st.session_state.form_data['query_complexity'] = st.select_slider("Overall Query Complexity", 
                                                                     options=["Very Simple", "Simple", "Moderate", "Complex", "Very Complex"],
                                                                     value=st.session_state.form_data.get('query_complexity', "Moderate"))

    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("Previous", key="prev_4"):
            prev_section()
    with col3:
        if st.button("Next: Other Workloads", key="next_4"):
            next_section()

# Other Workloads Section
elif st.session_state.current_section == 5:
    st.markdown("<h2 class='section-header'>Other Workloads</h2>", unsafe_allow_html=True)

    st.markdown("<p class='category-label'>Other Workloads</p>", unsafe_allow_html=True)

    # Ask if there are other workloads
    st.session_state.form_data['has_other_workloads'] = st.radio("Do you have other workloads to consider?", 
                                                                ["Yes", "No"],
                                                                index=["Yes", "No"].index(st.session_state.form_data.get('has_other_workloads', "No")))

    if st.session_state.form_data['has_other_workloads'] == "Yes":
        # Get number of other workloads
        st.session_state.form_data['other_workload_count'] = st.number_input("How many other workloads will you have?", 
                                                                            min_value=1, max_value=10, 
                                                                            value=int(st.session_state.form_data.get('other_workload_count', 1)))

        # For each other workload, collect details
        for i in range(int(st.session_state.form_data['other_workload_count'])):
            st.markdown(f"### Other Workload {i+1}")

            col1, col2 = st.columns(2)
            with col1:
                st.session_state.form_data[f'other_{i}_name'] = st.text_input("Workload Name", 
                                                                             key=f"other_{i}_name",
                                                                             value=st.session_state.form_data.get(f'other_{i}_name', f"Other Workload {i+1}"))

                st.session_state.form_data[f'other_{i}_type'] = st.selectbox("Workload Type",
                                                                            ["Data Science/ML", "Application Backend", "Data Sharing", 
                                                                             "Reporting", "Data API", "Other"],
                                                                            key=f"other_{i}_type",
                                                                            index=["Data Science/ML", "Application Backend", "Data Sharing", 
                                                                                   "Reporting", "Data API", "Other"].index(st.session_state.form_data.get(f'other_{i}_type', "Data Science/ML")))

                st.session_state.form_data[f'other_{i}_hours_per_day'] = st.slider("Average number of hours per day users use the tool", 
                                                                                  min_value=1, max_value=24, 
                                                                                  key=f"other_{i}_hours_per_day",
                                                                                  value=int(st.session_state.form_data.get(f'other_{i}_hours_per_day', 8)))

                st.session_state.form_data[f'other_{i}_days_per_month'] = st.slider("Average number of days per month users use the tool", 
                                                                                   min_value=1, max_value=31, 
                                                                                   key=f"other_{i}_days_per_month",
                                                                                   value=int(st.session_state.form_data.get(f'other_{i}_days_per_month', 22)))

            with col2:
                st.session_state.form_data[f'other_{i}_queries_per_day'] = st.number_input("Average number of queries/jobs per day", 
                                                                                          min_value=1, max_value=100000, 
                                                                                          key=f"other_{i}_queries_per_day",
                                                                                          value=int(st.session_state.form_data.get(f'other_{i}_queries_per_day', 500)))

                st.session_state.form_data[f'other_{i}_data_volume'] = st.number_input("Average data volume processed per query (GB)", 
                                                                                      min_value=0.1, max_value=10000.0, 
                                                                                      key=f"other_{i}_data_volume",
                                                                                      value=float(st.session_state.form_data.get(f'other_{i}_data_volume', 5.0)))

                st.session_state.form_data[f'other_{i}_peak_days'] = st.number_input("Average number of peak days in a month", 
                                                                                    min_value=1, max_value=31, 
                                                                                    key=f"other_{i}_peak_days",
                                                                                    value=int(st.session_state.form_data.get(f'other_{i}_peak_days', 5)))

                st.session_state.form_data[f'other_{i}_peaks_per_day'] = st.number_input("Average number of peaks per day", 
                                                                                        min_value=1, max_value=24, 
                                                                                        key=f"other_{i}_peaks_per_day",
                                                                                        value=int(st.session_state.form_data.get(f'other_{i}_peaks_per_day', 2)))

            col1, col2 = st.columns(2)
            with col1:
                st.session_state.form_data[f'other_{i}_peak_duration'] = st.number_input("Average duration of a peak (minutes)", 
                                                                                        min_value=1, max_value=1440, 
                                                                                        key=f"other_{i}_peak_duration",
                                                                                        value=int(st.session_state.form_data.get(f'other_{i}_peak_duration', 60)))

            with col2:
                st.session_state.form_data[f'other_{i}_concurrent_queries'] = st.number_input("Average number of queries running concurrently at peak", 
                                                                                             min_value=1, max_value=1000, 
                                                                                             key=f"other_{i}_concurrent_queries",
                                                                                             value=int(st.session_state.form_data.get(f'other_{i}_concurrent_queries', 10)))

    # Additional questions that might be helpful
    st.markdown("### Additional Considerations")

    st.session_state.form_data['geographic_distribution'] = st.multiselect("Geographic regions where users will access Snowflake",
                                                                          ["North America", "South America", "Europe", "Asia Pacific", 
                                                                           "Middle East", "Africa", "Australia/Oceania"],
                                                                          default=st.session_state.form_data.get('geographic_distribution', ["North America"]))

    st.session_state.form_data['high_availability_requirements'] = st.select_slider("High Availability Requirements", 
                                                                                   options=["Standard", "High", "Very High", "Mission Critical"],
                                                                                   value=st.session_state.form_data.get('high_availability_requirements', "Standard"))

    st.session_state.form_data['disaster_recovery_requirements'] = st.select_slider("Disaster Recovery Requirements", 
                                                                                   options=["Standard", "High", "Very High", "Mission Critical"],
                                                                                   value=st.session_state.form_data.get('disaster_recovery_requirements', "Standard"))

    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("Previous", key="prev_5"):
            prev_section()
    with col3:
        if st.button("Generate Summary & Recommendations", key="next_5"):
            next_section()
            st.session_state.show_summary = True

# Summary & Recommendations Section
elif st.session_state.current_section == 6 or st.session_state.show_summary:
    st.markdown("<h2 class='section-header'>Summary & Recommendations</h2>", unsafe_allow_html=True)

    # Calculate consumption estimates
    consumption_data = calculate_consumption_estimates()

    # Display key metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Initial Storage", f"{consumption_data['storage']['initial']:.1f} TB")

    with col2:
        st.metric("Final Storage (12 months)", f"{consumption_data['storage']['final']:.1f} TB")

    with col3:
        st.metric("Total Warehouses", len(consumption_data['compute']['estimates']))

    with col4:
        st.metric("Monthly Credits (at full scale)", f"{consumption_data['compute']['total_monthly_credits']:,.0f}")

    # Create and display charts
    storage_df, compute_df, warehouse_df = create_consumption_charts(consumption_data)

    # Detailed warehouse breakdown
    st.markdown("### 🏭 Detailed Warehouse Recommendations")

    # Format the warehouse data for display
    display_df = warehouse_df.copy()
    display_df['Monthly Credits'] = display_df['monthly_credits'].round(0).astype(int)
    display_df['Multi-Cluster'] = display_df['multi_cluster'].apply(lambda x: "Yes" if x else "No")
    display_df['Cluster Count'] = display_df['cluster_count']

    # Select columns for display
    display_columns = ['name', 'type', 'warehouse_size', 'credits_per_hour', 'Monthly Credits', 'Cluster Count', 'Multi-Cluster']
    display_df = display_df[display_columns]
    display_df.columns = ['Warehouse Name', 'Workload Type', 'Size', 'Credits/Hour', 'Monthly Credits', 'Clusters', 'Multi-Cluster']

    st.dataframe(display_df, use_container_width=True)

    # Cost estimates
    cost_data = display_cost_estimates(consumption_data)

    # Recommendations
    st.markdown("### 💡 Optimization Recommendations")

    recommendations = []

    # Storage recommendations
    storage_growth = consumption_data['storage']['final'] - consumption_data['storage']['initial']
    if storage_growth > 50:
        recommendations.append("📈 **High Storage Growth**: Consider implementing data lifecycle policies and archiving strategies")

    # Compute recommendations
    total_credits = consumption_data['compute']['total_monthly_credits']
    if total_credits > 10000:
        recommendations.append("⚡ **High Compute Usage**: Implement resource monitors and auto-suspend policies")

    # Multi-cluster recommendations
    multi_cluster_count = sum(1 for est in consumption_data['compute']['estimates'] if est['multi_cluster'])
    if multi_cluster_count > 0:
        recommendations.append(f"🔄 **Multi-Cluster Setup**: {multi_cluster_count} warehouses need multi-cluster configuration")

    # Cost optimization
    if cost_data['total_monthly'] > 50000:
        recommendations.append("💰 **Cost Optimization**: Consider reserved capacity or enterprise discounts")

    # Performance recommendations
    complex_queries = st.session_state.form_data.get('query_complexity', 'Moderate')
    if complex_queries in ['Complex', 'Very Complex']:
        recommendations.append("🚀 **Performance Tuning**: Implement clustering keys and result caching")

    # Security recommendations
    sensitivity = st.session_state.form_data.get('data_sensitivity', 'Internal')
    if sensitivity in ['Confidential', 'Restricted']:
        recommendations.append("🔒 **Security**: Implement column-level security and row access policies")

    for i, rec in enumerate(recommendations, 1):
        st.markdown(f"**{i}.** {rec}")

    # Save functionality
    st.markdown("---")
    st.markdown("### 💾 Save Sizing Information")

    save_name = st.session_state.form_data.get('customer_name', 'Customer')
    sizing_id = f"{save_name}_SIZING_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    if st.button("💾 Save to Snowflake Database", key="save_to_db"):
        saved_id = write_to_snowflake()
        if saved_id:
            st.balloons()
            st.success(f"✅ Sizing information saved with ID: **{saved_id}**")

    # Export options
    st.markdown("### 📤 Export Options")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📊 Export Charts as Images"):
            st.info("Chart export functionality - would save all charts as PNG files")

    with col2:
        if st.button("📋 Export Summary as CSV"):
            # Create summary CSV
            summary_data = {
                'Metric': ['Initial Storage (TB)', 'Final Storage (TB)', 'Total Warehouses', 'Monthly Credits', 'Monthly Cost ($)'],
                'Value': [
                    consumption_data['storage']['initial'],
                    consumption_data['storage']['final'],
                    len(consumption_data['compute']['estimates']),
                    consumption_data['compute']['total_monthly_credits'],
                    cost_data['total_monthly']
                ]
            }
            summary_df = pd.DataFrame(summary_data)
            csv = summary_df.to_csv(index=False)
            st.download_button("Download CSV", csv, f"{save_name}_summary.csv", "text/csv")

    with col3:
        if st.button("📄 Generate Report"):
            st.info("Full report generation - would create comprehensive PDF report - Future")

    st.markdown("---")
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Previous", key="prev_6"):
            prev_section()
            st.session_state.show_summary = False
    with col2:
        if st.button("View Pricing Details", key="next_6"):
            st.info("Full Pricing Details - would create comprehensive PDF report - Future")
            next_section()
