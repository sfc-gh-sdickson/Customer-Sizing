import streamlit as st
import pandas as pd
import datetime
import plotly.graph_objects as go
import plotly.express as px
import numpy as np


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

svg_content = read_svg("Snowflake.svg")
st.image(svg_content, width=100)

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
    "Summary & Recommendations",
    "Pricing Recommendations"
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

        today = datetime.date.today()
        default_dev_start = today + datetime.timedelta(days=30)
        default_go_live = today + datetime.timedelta(days=90)

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

    # Calculate storage requirements
    initial_storage = float(st.session_state.form_data.get('initial_raw_volume', 0))
    final_storage = float(st.session_state.form_data.get('final_raw_volume', 0))

    # Estimate storage with compression and additional copies
    compression_factor = 0.3  # Assuming 70% compression
    redundancy_factor = 1.5   # Accounting for Time Travel, Fail-safe, etc.

    initial_storage_with_factors = initial_storage * compression_factor * redundancy_factor
    final_storage_with_factors = final_storage * compression_factor * redundancy_factor

    # Calculate monthly storage growth
    monthly_growth = (final_storage_with_factors - initial_storage_with_factors) / 12

    # Estimate warehouse sizes based on workloads
    warehouse_sizes = []

    # For ETL/ELT
    pipeline_count = int(st.session_state.form_data.get('pipeline_count', 0))
    for i in range(pipeline_count):
        volume_per_job = float(st.session_state.form_data.get(f'pipeline_{i}_volume_per_job', 0))
        concurrent_jobs = int(st.session_state.form_data.get(f'pipeline_{i}_concurrent_jobs', 0))

        # Simple heuristic for warehouse size
        if volume_per_job * concurrent_jobs < 50:
            size = "X-Small"
        elif volume_per_job * concurrent_jobs < 200:
            size = "Small"
        elif volume_per_job * concurrent_jobs < 500:
            size = "Medium"
        elif volume_per_job * concurrent_jobs < 1000:
            size = "Large"
        else:
            size = "X-Large"

        warehouse_sizes.append({
            "name": st.session_state.form_data.get(f'pipeline_{i}_name', f"Pipeline {i+1}"),
            "type": "ETL/ELT",
            "size": size,
            "multi_cluster": concurrent_jobs > 5
        })

    # For Analytics
    analytics_count = int(st.session_state.form_data.get('analytics_workload_count', 0))
    for i in range(analytics_count):
        concurrent_queries = int(st.session_state.form_data.get(f'analytics_{i}_concurrent_queries', 0))
        power_users_pct = int(st.session_state.form_data.get(f'analytics_{i}_power_users', 0))

        # Simple heuristic for warehouse size
        if concurrent_queries < 10 and power_users_pct < 20:
            size = "X-Small"
        elif concurrent_queries < 30 and power_users_pct < 40:
            size = "Small"
        elif concurrent_queries < 60 and power_users_pct < 60:
            size = "Medium"
        elif concurrent_queries < 100:
            size = "Large"
        else:
            size = "X-Large"

        warehouse_sizes.append({
            "name": st.session_state.form_data.get(f'analytics_{i}_name', f"Analytics {i+1}"),
            "type": "Analytics",
            "size": size,
            "multi_cluster": concurrent_queries > 20
        })

    # For Other Workloads
    if st.session_state.form_data.get('has_other_workloads', "No") == "Yes":
        other_count = int(st.session_state.form_data.get('other_workload_count', 0))
        for i in range(other_count):
            concurrent_queries = int(st.session_state.form_data.get(f'other_{i}_concurrent_queries', 0))
            data_volume = float(st.session_state.form_data.get(f'other_{i}_data_volume', 0))

            # Simple heuristic for warehouse size
            if concurrent_queries < 10 and data_volume < 10:
                size = "X-Small"
            elif concurrent_queries < 30 and data_volume < 50:
                size = "Small"
            elif concurrent_queries < 60 and data_volume < 200:
                size = "Medium"
            elif concurrent_queries < 100:
                size = "Large"
            else:
                size = "X-Large"

            warehouse_sizes.append({
                "name": st.session_state.form_data.get(f'other_{i}_name', f"Other {i+1}"),
                "type": st.session_state.form_data.get(f'other_{i}_type', "Other"),
                "size": size,
                "multi_cluster": concurrent_queries > 15
            })

    # Display summary
    st.markdown("<div class='summary-box'>", unsafe_allow_html=True)
    st.markdown("## Customer Environment Size Prediction")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Storage Requirements")
        st.markdown(f"**Initial Storage (Month 1):** {initial_storage_with_factors:.2f} TB")
        st.markdown(f"**Final Storage (Month 12):** {final_storage_with_factors:.2f} TB")
        st.markdown(f"**Monthly Growth Rate:** {monthly_growth:.2f} TB/month")

        # Create storage growth chart
        months = list(range(1, 13))
        storage_values = [initial_storage_with_factors + (monthly_growth * i) for i in range(12)]

        storage_df = pd.DataFrame({
            'Month': months,
            'Storage (TB)': storage_values
        })

        fig = px.line(storage_df, x='Month', y='Storage (TB)',
                      title='Projected Storage Growth',
                      markers=True)
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### Compute Requirements")
        st.markdown(f"**Recommended Number of Warehouses:** {len(warehouse_sizes)}")

        # Create warehouse size chart
        size_map = {"X-Small": 1, "Small": 2, "Medium": 3, "Large": 4, "X-Large": 5}
        warehouse_df = pd.DataFrame(warehouse_sizes)
        warehouse_df['size_num'] = warehouse_df['size'].map(size_map)
        warehouse_df['multi_cluster_text'] = warehouse_df['multi_cluster'].apply(lambda x: "Yes" if x else "No")

        fig = px.bar(warehouse_df, x='name', y='size_num', color='type',
                     title='Recommended Warehouse Sizes',
                     labels={'size_num': 'Size', 'name': 'Warehouse', 'type': 'Workload Type'},
                     hover_data=['size', 'multi_cluster_text'],
                     category_orders={"size_num": [1, 2, 3, 4, 5]})

        fig.update_layout(height=300)
        fig.update_yaxes(tickvals=[1, 2, 3, 4, 5],
                         ticktext=["X-Small", "Small", "Medium", "Large", "X-Large"])
        st.plotly_chart(fig, use_container_width=True)

    # Price Estimate Section
elif st.session_state.current_section == 7 or st.session_state.show_summary:
    st.markdown("<h2 class='section-header'>Price Estimate</h2>", unsafe_allow_html=True)

    # Calculate storage requirements
    initial_storage = float(st.session_state.form_data.get('initial_raw_volume', 0))
    final_storage = float(st.session_state.form_data.get('final_raw_volume', 0))

    # Estimate storage with compression and additional copies
    compression_factor = 0.3  # Assuming 70% compression
    redundancy_factor = 1.5   # Accounting for Time Travel, Fail-safe, etc.

    initial_storage_with_factors = initial_storage * compression_factor * redundancy_factor
    final_storage_with_factors = final_storage * compression_factor * redundancy_factor
    storage_costs = final_storage_with_factors * 23

    # Calculate monthly storage growth
    monthly_growth = (final_storage_with_factors - initial_storage_with_factors) / 12


    st.markdown("### Detailed Warehouse Recommendations")
    warehouse_display = pd.DataFrame(warehouse_sizes)[['name', 'type', 'size', 'multi_cluster']]
    warehouse_display['multi_cluster'] = warehouse_display['multi_cluster'].apply(lambda x: "Yes" if x else "No")
    warehouse_display.columns = ['Warehouse Name', 'Workload Type', 'Size', 'Multi-cluster']
    st.table(warehouse_display)

    st.markdown("### Additional Recommendations")

    # Generate recommendations based on the data
    recommendations = []

    # Storage recommendations
    if final_storage > 100:
        recommendations.append("Consider implementing a data lifecycle management strategy to archive older data.")

    # Compute recommendations
    if any(w['multi_cluster'] for w in warehouse_sizes):
        recommendations.append("Configure multi-cluster warehouses for workloads with high concurrency requirements.")

    # Performance recommendations
    if st.session_state.form_data.get('query_complexity', "Moderate") in ["Complex", "Very Complex"]:
        recommendations.append("Implement proper clustering keys and materialized views to optimize complex query performance.")

    # Cost optimization
    recommendations.append("Set up resource monitors to track and control warehouse usage.")
    recommendations.append("Configure auto-suspend and auto-resume for all warehouses to minimize idle time.")

    # Security recommendations
    if st.session_state.form_data.get('data_sensitivity', "Internal") in ["Confidential", "Restricted"]:
        recommendations.append("Implement column-level security and row access policies for sensitive data.")

    # Display recommendations
    for i, rec in enumerate(recommendations):
        st.markdown(f"**{i+1}.** {rec}")

    st.markdown("</div>", unsafe_allow_html=True)

    # Export options
    st.markdown("### Export Options")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Export as PDF"):
            st.info("PDF export functionality would be implemented here.")
    with col2:
        if st.button("Export as Excel"):
            st.info("Excel export functionality would be implemented here.")

    st.markdown("---")
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Previous", key="prev_6"):
            prev_section()
            st.session_state.show_summary = False
