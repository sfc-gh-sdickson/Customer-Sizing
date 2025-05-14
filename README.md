# Snowflake Customer Sizing Tool ❄️

<img src="Snowflake.svg" width="75">

A Streamlit-based application designed to help technical teams accurately predict storage and compute requirements for new Snowflake implementations. This tool guides users through a structured data collection process and generates detailed sizing recommendations.

## Features ✨

- **Multi-Section Workflow**: Guided questionnaire across 8 key technical areas
- **Dynamic Form Handling**: Adaptive inputs based on user responses
- **Storage Projections**: 12-month storage growth visualization
- **Compute Recommendations**: Warehouse sizing based on workload analysis
- **Interactive Visualizations**: Plotly charts for data exploration
- **Export Capabilities**: PDF/Excel reporting (stub implementation)

## Installation 🛠️

1. **Clone Repository**
   ```bash
   git clone https://github.com/your-username/snowflake-sizing-tool.git
   cd snowflake-sizing-tool

## Install Dependencies

streamlit==1.28.0
pandas==2.0.3
plotly==5.18.0
numpy==1.24.3

## Run Application

Copy into Streamlit in Snowflake with supporting files.  We sure to setup the required libraries

## Usage 🖥️
Navigate through sections using the sidebar
Input technical specifications for:
Data sources and volumes
ETL/ELT pipeline configurations
Analytics workload patterns
Additional workload requirements
View interactive projections and recommendations
Export results (PDF/Excel placeholder functionality)

## Application Structure 📂
Section	Description
1. Customer Information	Basic organizational details
2. Use Case Timeline	Project milestones and success metrics
3. Technical Overview	Data sources and system architecture
4. Data Loading & Transformation	ETL pipeline configurations
5. Analytics Workload	BI tool usage patterns
6. Other Workloads	ML/Data Science requirements
7. Summary & Recommendations	Storage/compute projections
8. Pricing Recommendations	Cost estimation (placeholder)

## Technical Specifications ⚙️
Python: 3.9+
Frontend: Streamlit
Visualization: Plotly
Data Handling: Pandas/Numpy
Session Management: Streamlit Session State

## Contributing 🤝
Fork the repository
Create feature branch (git checkout -b feature/improvement)
Commit changes (git commit -am 'Add new feature')
Push to branch (git push origin feature/improvement)
Open Pull Request
## Disclaimer ⚠️
This tool provides approximate estimates based on standard Snowflake architecture patterns. Actual requirements may vary based on specific use cases and workload patterns. Always validate recommendations with Snowflake architectural best practices.
