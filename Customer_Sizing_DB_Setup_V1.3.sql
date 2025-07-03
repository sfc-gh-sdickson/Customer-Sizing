/*-----------------------------------------------------------------------------------------*/
  -- Database Objects for the Customer Sizing V1.3 Streamlit App
  -- Customer_Sizing_V1.3.sql
  -- Repo: https://github.com/sfc-gh-sdickson/Customer-Sizing
  -- 3-Jul-2025 Author: Stephen Dickson
  -- Stephen.Dickson@Snowflake.com
/*-----------------------------------------------------------------------------------------*/

create or replace DATABASE SIZING_TOOL;
create or replace SCHEMA CUSTOMER_SIZING;
use SCHEMA SIZING_TOOL.CUSTOMER_SIZING;

/*---------------------- New Sizing_Main --------------------------------*/

CREATE OR REPLACE TABLE SIZING_TOOL.CUSTOMER_SIZING.SIZING_MAIN (
	SIZING_ID VARCHAR(50) NOT NULL,
	CUSTOMER_NAME VARCHAR(255),
	INDUSTRY VARCHAR(100),
	CONTACT_NAME VARCHAR(255),
	CONTACT_EMAIL VARCHAR(255),
	COMPANY_SIZE VARCHAR(100),
	EXISTING_DATA_PLATFORM VARCHAR(255),
	BUSINESS_OWNER VARCHAR(255),
	TECH_OWNER VARCHAR(255),
	DEV_START_DATE DATE,
	GO_LIVE_DATE DATE,
	SUCCESS_METRICS VARCHAR(16777216),
	ROADBLOCKS VARCHAR(16777216),
	RAMP_UP_CURVE VARCHAR(50),
	DATA_SOURCES_COUNT NUMBER(38,0),
	INITIAL_RAW_VOLUME_TB FLOAT,
	FINAL_RAW_VOLUME_TB FLOAT,
	ANNUAL_GROWTH_RATE NUMBER(38,0), -- New Column
	TOOLS VARCHAR(255),
	DATA_RETENTION_PERIOD NUMBER(38,0),
	DATA_SENSITIVITY VARCHAR(50),
	EXPECTED_WAREHOUSES NUMBER(38,0),
	TOTAL_USERS NUMBER(38,0),
	QUERY_COMPLEXITY VARCHAR(50),
	HAS_OTHER_WORKLOADS VARCHAR(10),
	OTHER_WORKLOAD_COUNT NUMBER(38,0), -- New Column
	GEOGRAPHIC_DISTRIBUTION VARCHAR(255),
	HIGH_AVAILABILITY_REQUIREMENTS VARCHAR(50),
	DISASTER_RECOVERY_REQUIREMENTS VARCHAR(50),
	CREATED_TIMESTAMP TIMESTAMP_NTZ(9) DEFAULT CURRENT_TIMESTAMP(),
	PRIMARY KEY (SIZING_ID)
);

/*---------------------- End New Sizing_Main --------------------------------*/

create or replace TABLE SIZING_TOOL.CUSTOMER_SIZING.ANALYTICS_WORKLOADS (
	SIZING_ID VARCHAR(50),
	ANALYTICS_INDEX NUMBER(38,0),
	WORKLOAD_NAME VARCHAR(255),
	PRIMARY_TOOL VARCHAR(100),
	HOURS_PER_DAY NUMBER(38,0),
	DAYS_PER_MONTH NUMBER(38,0),
	QUERIES_PER_DAY NUMBER(38,0),
	BASIC_USERS_PCT NUMBER(38,0),
	EXPERT_USERS_PCT NUMBER(38,0),
	POWER_USERS_PCT NUMBER(38,0),
	PEAK_DAYS NUMBER(38,0),
	PEAKS_PER_DAY NUMBER(38,0),
	PEAK_DURATION_MINUTES NUMBER(38,0),
	CONCURRENT_QUERIES NUMBER(38,0),
	CACHING_PCT NUMBER(38,0),
	CREATED_TIMESTAMP TIMESTAMP_NTZ(9) DEFAULT CURRENT_TIMESTAMP()
);

create or replace TABLE SIZING_TOOL.CUSTOMER_SIZING.DATA_SOURCES (
	SIZING_ID VARCHAR(50),
	SOURCE_INDEX NUMBER(38,0),
	SOURCE_NAME VARCHAR(255),
	SOURCE_TYPE VARCHAR(100),
	CURRENT_VOLUME_TB FLOAT,
	CREATED_TIMESTAMP TIMESTAMP_NTZ(9) DEFAULT CURRENT_TIMESTAMP()
);

create or replace TABLE SIZING_TOOL.CUSTOMER_SIZING.OTHER_WORKLOADS (
	SIZING_ID VARCHAR(50),
	OTHER_INDEX NUMBER(38,0),
	WORKLOAD_NAME VARCHAR(255),
	WORKLOAD_TYPE VARCHAR(100),
	HOURS_PER_DAY NUMBER(38,0),
	DAYS_PER_MONTH NUMBER(38,0),
	QUERIES_PER_DAY NUMBER(38,0),
	DATA_VOLUME_GB FLOAT,
	PEAK_DAYS NUMBER(38,0),
	PEAKS_PER_DAY NUMBER(38,0),
	PEAK_DURATION_MINUTES NUMBER(38,0),
	CONCURRENT_QUERIES NUMBER(38,0),
	CREATED_TIMESTAMP TIMESTAMP_NTZ(9) DEFAULT CURRENT_TIMESTAMP()
);

create or replace TABLE SIZING_TOOL.CUSTOMER_SIZING.OTHER_WORKLOADS (
	SIZING_ID VARCHAR(50),
	OTHER_INDEX NUMBER(38,0),
	WORKLOAD_NAME VARCHAR(255),
	WORKLOAD_TYPE VARCHAR(100),
	HOURS_PER_DAY NUMBER(38,0),
	DAYS_PER_MONTH NUMBER(38,0),
	QUERIES_PER_DAY NUMBER(38,0),
	DATA_VOLUME_GB FLOAT,
	PEAK_DAYS NUMBER(38,0),
	PEAKS_PER_DAY NUMBER(38,0),
	PEAK_DURATION_MINUTES NUMBER(38,0),
	CONCURRENT_QUERIES NUMBER(38,0),
	CREATED_TIMESTAMP TIMESTAMP_NTZ(9) DEFAULT CURRENT_TIMESTAMP()
);

create or replace TABLE SIZING_TOOL.CUSTOMER_SIZING.PIPELINES (
	SIZING_ID VARCHAR(50),
	PIPELINE_INDEX NUMBER(38,0),
	PIPELINE_NAME VARCHAR(255),
	FREQUENCY VARCHAR(100),
	JOBS_PER_DAY NUMBER(38,0),
	VOLUME_PER_JOB_GB FLOAT,
	RUNTIME_MINUTES NUMBER(38,0),
	DAYS_PER_MONTH NUMBER(38,0),
	CONCURRENT_JOBS NUMBER(38,0),
	PEAK_DURATION_MINUTES NUMBER(38,0),
	CREATED_TIMESTAMP TIMESTAMP_NTZ(9) DEFAULT CURRENT_TIMESTAMP()
);

        
--------------------------------
-- Clone Section
--------------------------------
Create schema CUSTOMER_SIZING_ARCHIVE;

/*---------------------- Backup Clones --------------------------------*/

Create table SIZING_TOOL.CUSTOMER_SIZING_ARCHIVE.SIZING_MAIN_RECOVERY
Clone SIZING_TOOL.CUSTOMER_SIZING.SIZING_MAIN;

Create table SIZING_TOOL.CUSTOMER_SIZING_ARCHIVE.ANALYTICS_WORKLOADS_RECOVERY
Clone SIZING_TOOL.CUSTOMER_SIZING.ANALYTICS_WORKLOADS;

Create table SIZING_TOOL.CUSTOMER_SIZING_ARCHIVE.PIPELINES_RECOVERY
Clone SIZING_TOOL.CUSTOMER_SIZING.PIPELINES;

Create table SIZING_TOOL.CUSTOMER_SIZING_ARCHIVE.DATA_SOURCES_RECOVERY
Clone SIZING_TOOL.CUSTOMER_SIZING.DATA_SOURCES;

Create table SIZING_TOOL.CUSTOMER_SIZING_ARCHIVE.OTHER_WORKLOADS_RECOVERY
Clone SIZING_TOOL.CUSTOMER_SIZING.OTHER_WORKLOADS;

/*---------------------- Backup Clones --------------------------------*/

/*---------------------- Restore Clones --------------------------------*/
CREATE OR REPLACE TABLE SIZING_TOOL.CUSTOMER_SIZING.SIZING_MAIN
CLONE SIZING_TOOL.CUSTOMER_SIZING_ARCHIVE.SIZING_MAIN_RECOVERY;

CREATE OR REPLACE TABLE SIZING_TOOL.CUSTOMER_SIZING.OTHER_WORKLOADS
CLONE SIZING_TOOL.CUSTOMER_SIZING_ARCHIVE.OTHER_WORKLOADS_RECOVERY;

CREATE OR REPLACE TABLE SIZING_TOOL.CUSTOMER_SIZING.DATA_SOURCES
CLONE SIZING_TOOL.CUSTOMER_SIZING_ARCHIVE.DATA_SOURCES_RECOVERY;

CREATE OR REPLACE TABLE SIZING_TOOL.CUSTOMER_SIZING.PIPELINES
CLONE SIZING_TOOL.CUSTOMER_SIZING_ARCHIVE.PIPELINES_RECOVERY;

CREATE OR REPLACE TABLE SIZING_TOOL.CUSTOMER_SIZING.ANALYTICS_WORKLOADS
CLONE SIZING_TOOL.CUSTOMER_SIZING_ARCHIVE.ANALYTICS_WORKLOADS_RECOVERY;

/*---------------------- Restore Clones --------------------------------*/


/*----------------------  Generated Testing Data Inserts --------------------------------*/

select * from SIZING_TOOL.CUSTOMER_SIZING.DATA_SOURCES;

INSERT INTO SIZING_TOOL.CUSTOMER_SIZING.SIZING_MAIN VALUES
('SZ001', 'DataDragon Analytics', 'Retail', 'Sarah Chen', 'sarah.chen@datadragon.com', 'Enterprise', '["Oracle"]', 'Michael Torres', 'Jennifer Wu', '2025-01-15', '2025-04-01', 'Reduce query time by 60%, Enable real-time analytics', 'Legacy system migration, Team training', 'Gradual', 5, 150.0, 500.0, 35, '["Tableau","PowerBI","Python"]', 365, 'High', 8, 250, 'Complex', 'Yes', 3, '["US","Europe","Asia"]', 'Critical', 'Required', '2024-05-02 14:23:11'),
('SZ002', 'CloudCrunch Corp', 'Finance', 'David Smith', 'dsmith@cloudcrunch.com', 'Large', '["SQL Server"]', 'Lisa Anderson', 'Robert Brown', '2025-02-01', '2025-05-15', 'Improve data freshness, Reduce costs by 40%', 'Regulatory compliance, Data governance', 'Aggressive', 8, 80.0, 350.0, 45, '["Looker","Excel","R"]', 730, 'Critical', 6, 180, 'Medium', 'Yes', 2, '["US","Canada"]', 'High', 'Required', '2024-06-10 09:12:45'),
('SZ003', 'ByteBazaar Inc', 'E-commerce', 'Emma Wilson', 'emma@bytebazaar.com', 'Medium', '["MySQL","MongoDB"]', 'John Davis', 'Maria Garcia', '2025-01-20', '2025-03-30', 'Scale to handle Black Friday traffic, Real-time inventory', 'NoSQL to SQL migration', 'Moderate', 6, 45.0, 180.0, 50, '["Qlik","Tableau"]', 180, 'Medium', 5, 120, 'Complex', 'No', 0, '["US"]', 'Medium', 'Optional', '2024-04-28 17:55:02'),
('SZ004', 'NeuralNest AI', 'Technology', 'Alex Johnson', 'ajohnson@neuralnest.ai', 'Startup', '["PostgreSQL"]', 'Sophie Turner', 'Kevin Lee', '2025-02-15', '2025-06-01', 'Enable ML model training on data warehouse', 'Limited budget, Small team', 'Gradual', 3, 20.0, 100.0, 60, '["Python"]', 90, 'Low', 3, 50, 'Simple', 'Yes', 4, '["US"]', 'Low', 'Optional', '2024-05-19 11:08:37'),
('SZ005', 'MegaMart Global', 'Retail', 'Patricia Brown', 'pbrown@megamart.com', 'Enterprise', '["Teradata"]', 'Charles Wilson', 'Nancy Taylor', '2025-01-10', '2025-04-20', 'Consolidate global data, 24/7 availability', 'Multiple time zones, Large data volumes', 'Phased', 12, 800.0, 2000.0, 30, '["MicroStrategy","SAP"]', 1095, 'High', 15, 500, 'Complex', 'Yes', 5, '["Global"]', 'Critical', 'Required', '2024-06-22 08:44:19'),
('SZ006', 'HealthHub Solutions', 'Healthcare', 'Dr. James Miller', 'jmiller@healthhub.com', 'Large', '["Oracle","SQL Server"]', 'Susan Martinez', 'Thomas Anderson', '2025-03-01', '2025-07-01', 'HIPAA compliance, Patient analytics', 'Sensitive data, Strict regulations', 'Moderate', 7, 120.0, 400.0, 25, '["SAS","Tableau","R"]', 2555, 'Critical', 10, 300, 'Medium', 'Yes', 3, '["US"]', 'High', 'Required', '2024-05-30 16:31:55'),
('SZ007', 'StreamFlix Entertainment', 'Media', 'Jessica Lee', 'jlee@streamflix.com', 'Large', '["Cassandra","Hadoop"]', 'Ryan Cooper', 'Michelle White', '2025-01-25', '2025-05-10', 'Real-time viewer analytics, Personalization', 'Massive scale, Streaming data', 'Aggressive', 9, 300.0, 1200.0, 40, '["Spark","Kafka","Python"]', 365, 'Medium', 12, 400, 'Complex', 'Yes', 6, '["US","Europe"]', 'Critical', 'Required', '2024-06-05 13:17:28'),
('SZ008', 'GreenEnergy Dynamics', 'Energy', 'Robert Taylor', 'rtaylor@greenenergy.com', 'Medium', '["Hadoop","SQL Server"]', 'Amanda Clark', 'Daniel Rodriguez', '2025-02-20', '2025-06-15', 'IoT sensor analytics, Predictive maintenance', 'Time-series data, Edge computing', 'Gradual', 4, 60.0, 250.0, 55, '["PowerBI"]', 730, 'Medium', 7, 150, 'Complex', 'Yes', 2, '["US","Mexico"]', 'High', 'Optional', '2024-04-18 10:22:09'),
('SZ009', 'QuickShip Logistics', 'Transportation', 'Michael Zhang', 'mzhang@quickship.com', 'Large', '["Oracle DB"]', 'Jennifer Lopez', 'Steven Kim', '2025-01-30', '2025-04-30', 'Route optimization, Real-time tracking', 'Legacy systems, API integration', 'Moderate', 8, 90.0, 380.0, 35, '["Tableau","Python","Excel"]', 365, 'Medium', 9, 280, 'Medium', 'Yes', 4, '["North America"]', 'High', 'Required', '2024-06-15 19:41:03'),
('SZ010', 'TechnoTrend Analytics', 'Consulting', 'Lisa Park', 'lpark@technotrend.com', 'Small', '["Various Client Systems"]', 'Brian Wilson', 'Carol Davis', '2025-03-15', '2025-06-30', 'Multi-tenant analytics, Client reporting', 'Data isolation, Varied schemas', 'Phased', 15, 40.0, 200.0, 50, '["Tableau", "Power BI"]', 365, 'High', 20, 100, 'Complex', 'Yes', 8, '["US"]', 'Medium', 'Required', '2024-05-11 07:55:44'),
('SZ011', 'FoodieChain Restaurants', 'Food Service', 'Carlos Martinez', 'cmartinez@foodiechain.com', 'Medium', '["MySQL"]', 'Elena Rodriguez', 'Frank Thompson', '2025-02-05', '2025-05-20', 'Inventory optimization, Customer analytics', 'Franchise data consolidation', 'Moderate', 10, 30.0, 150.0, 45, '["Looker","Excel"]', 180, 'Low', 6, 180, 'Simple', 'No', 0, '["North America"]', 'Medium', 'Optional', '2024-04-25 21:13:22'),
('SZ012', 'CryptoVault Exchange', 'Finance', 'Wei Chen', 'wchen@cryptovault.com', 'Medium', '["PostgreSQL","Redis"]', 'Natasha Volkov', 'James Park', '2025-01-18', '2025-04-15', '24/7 trading analytics, Fraud detection', 'High-frequency data, Security', 'Aggressive', 5, 150.0, 600.0, 70, '["Looker","Python"]', 90, 'Critical', 8, 200, 'Complex', 'Yes', 3, '["Global"]', 'Critical', 'Required', '2024-06-01 12:09:18'),
('SZ013', 'EduTech Academy', 'Education', 'Dr. Sarah Williams', 'swilliams@edutech.edu', 'Large', '["PostgreSQL","MySQL"]', 'Mark Johnson', 'Linda Brown', '2025-03-10', '2025-08-01', 'Student performance analytics, Course optimization', 'Academic calendar, Privacy concerns', 'Gradual', 6, 25.0, 120.0, 30, '["Tableau","R","Python"]', 1825, 'Medium', 5, 150, 'Medium', 'Yes', 2, '["US"]', 'Medium', 'Optional', '2024-05-27 15:36:50'),
('SZ014', 'SmartCity Solutions', 'Government', 'John Adams', 'jadams@smartcity.gov', 'Enterprise', '["Oracle","SAP"]', 'Rachel Green', 'Tom Anderson', '2025-02-25', '2025-07-15', 'Citizen services analytics, IoT integration', 'Government regulations, Public data', 'Phased', 20, 200.0, 800.0, 25, '["SAP","Tableau","PowerBI"]', 2920, 'High', 12, 350, 'Complex', 'Yes', 5, '["US"]', 'High', 'Required', '2024-06-18 18:27:39'),
('SZ015', 'BioPharma Innovations', 'Pharmaceutical', 'Dr. Emily Chen', 'echen@biopharma.com', 'Large', '["SAP","SQL Server"]', 'Richard Moore', 'Jessica Taylor', '2025-01-12', '2025-05-01', 'Clinical trial analytics, Drug discovery', 'FDA compliance, Data validation', 'Moderate', 8, 180.0, 700.0, 35, '["SAS","R","Spotfire"]', 3650, 'Critical', 10, 250, 'Complex', 'Yes', 4, '["US","Europe","Asia"]', 'Critical', 'Required', '2024-05-06 20:49:07'),
('SZ016', 'GameVerse Studios', 'Gaming', 'Tyler Jackson', 'tjackson@gameverse.com', 'Medium', '["MongoDB","DynamoDB"]', 'Ashley Martinez', 'Chris Lee', '2025-02-08', '2025-05-25', 'Player behavior analytics, Live ops', 'Real-time requirements, Global scale', 'Aggressive', 7, 100.0, 500.0, 60, '["Spotfire","SAS"]', 365, 'Medium', 8, 300, 'Complex', 'Yes', 5, '["Global"]', 'High', 'Required', '2024-04-30 18:02:33'),
('SZ017', 'AutoDrive Motors', 'Automotive', 'Hans Mueller', 'hmueller@autodrive.com', 'Enterprise', '["SAP","Oracle"]', 'Sofia Andersson', 'Raj Patel', '2025-01-22', '2025-06-10', 'Manufacturing analytics, Supply chain optimization', 'Global operations, Multiple ERPs', 'Phased', 11, 250.0, 1000.0, 40, '["Qlik","SAS"]', 1095, 'High', 14, 400, 'Complex', 'Yes', 6, '["Global"]', 'Critical', 'Required', '2024-06-12 22:15:59'),
('SZ018', 'InsureWise Corp', 'Insurance', 'Barbara Thompson', 'bthompson@insurewise.com', 'Large', '["Guidewire","SQL Server"]', 'David Clark', 'Emma Wilson', '2025-03-05', '2025-07-20', 'Risk analytics, Claims prediction', 'Actuarial models, Regulatory reporting', 'Moderate', 9, 140.0, 550.0, 30, '["SAS","Tableau","Excel"]', 2555, 'High', 11, 320, 'Complex', 'Yes', 3, '["US","Canada"]', 'High', 'Required', '2024-05-15 06:38:14'),
('SZ019', 'FashionForward Retail', 'Retail', 'Isabella Rossi', 'irossi@fashionforward.com', 'Medium', '["Netezza","MySQL"]', 'Marcus Johnson', 'Olivia Brown', '2025-01-28', '2025-04-25', 'Trend analytics, Inventory optimization', 'Seasonal patterns, Multi-channel', 'Moderate', 7, 50.0, 220.0, 45, '["Looker","PowerBI"]', 730, 'Medium', 7, 180, 'Medium', 'Yes', 2, '["US","Europe"]', 'Medium', 'Optional', '2024-06-08 03:29:41'),
('SZ020', 'TeleConnect Networks', 'Telecommunications', 'Ahmed Hassan', 'ahassan@teleconnect.com', 'Enterprise', '["Oracle","Netezza"]', 'Laura Martinez', 'Peter Wong', '2025-02-12', '2025-06-05', 'Network analytics, Customer churn prediction', 'Massive data volumes, Real-time processing', 'Aggressive', 13, 500.0, 2500.0, 50, '["MicroStrategy","Python","Spark"]', 1095, 'Critical', 18, 600, 'Complex', 'Yes', 7, '["US"]', 'Critical', 'Required', '2024-05-23 23:57:26');

-- ANALYTICS_WORKLOADS TABLE INSERTS (50 rows total, distributed across the 20 sizing IDs)
select * from SIZING_TOOL.CUSTOMER_SIZING.ANALYTICS_WORKLOADS;

INSERT INTO SIZING_TOOL.CUSTOMER_SIZING.ANALYTICS_WORKLOADS VALUES
-- SZ001 workloads
('SZ001', 1, 'Sales Dashboard Analytics', 'Tableau', 16, 30, 5000, 60, 30, 10, 5, 3, 60, 50, 70, '2024-05-28 14:23:00'),
('SZ001', 2, 'Inventory Forecasting', 'Python', 8, 20, 1000, 20, 50, 30, 10, 2, 120, 20, 40, '2024-04-15 09:12:00'),
('SZ001', 3, 'Customer Segmentation', 'Power BI', 12, 25, 3000, 50, 35, 15, 8, 4, 45, 30, 60, '2024-06-03 17:45:00'),
-- SZ002 workloads
('SZ002', 1, 'Risk Analytics', 'Looker', 24, 30, 8000, 40, 40, 20, 20, 5, 90, 80, 50, '2024-05-10 11:00:00'),
('SZ002', 2, 'Regulatory Reporting', 'Excel', 10, 20, 500, 70, 20, 10, 5, 1, 30, 10, 80, '2024-04-22 08:30:00'),
('SZ002', 3, 'Trading Analytics', 'R', 18, 22, 10000, 10, 30, 60, 22, 10, 60, 100, 30, '2024-06-01 13:15:00'),
-- SZ003 workloads
('SZ003', 1, 'Product Performance', 'Tableau', 14, 30, 4000, 55, 30, 15, 10, 4, 45, 40, 65, '2024-05-05 10:00:00'),
('SZ003', 2, 'Customer Journey Analysis', 'Qlik', 16, 28, 6000, 45, 35, 20, 15, 6, 60, 60, 55, '2024-04-18 15:30:00'),
-- SZ004 workloads
('SZ004', 1, 'Model Training Pipeline', 'Python', 20, 25, 2000, 10, 20, 70, 5, 8, 180, 30, 20, '2024-05-20 12:00:00'),
('SZ004', 2, 'Data Exploration', 'Jupyter', 12, 30, 1500, 20, 30, 50, 8, 5, 60, 25, 40, '2024-06-07 09:00:00'),
-- SZ005 workloads
('SZ005', 1, 'Global Sales Analytics', 'MicroStrategy', 24, 30, 15000, 50, 35, 15, 30, 8, 120, 150, 60, '2024-04-25 16:00:00'),
('SZ005', 2, 'Supply Chain Optimization', 'SAP', 24, 30, 8000, 40, 40, 20, 20, 6, 90, 100, 70, '2024-05-15 10:30:00'),
('SZ005', 3, 'Store Performance', 'MicroStrategy', 18, 30, 10000, 60, 30, 10, 25, 5, 60, 120, 65, '2024-06-02 14:00:00'),
-- SZ006 workloads
('SZ006', 1, 'Patient Outcomes Analysis', 'SAS', 16, 30, 3000, 30, 50, 20, 10, 3, 90, 40, 50, '2024-05-12 11:30:00'),
('SZ006', 2, 'Clinical Dashboard', 'Tableau', 24, 30, 6000, 60, 30, 10, 15, 4, 45, 60, 70, '2024-04-20 13:00:00'),
('SZ006', 3, 'Research Analytics', 'R', 12, 25, 2000, 10, 40, 50, 8, 2, 120, 30, 40, '2024-06-05 15:00:00'),
-- SZ007 workloads
('SZ007', 1, 'Viewer Analytics', 'Spark', 24, 30, 20000, 40, 35, 25, 30, 10, 60, 200, 45, '2024-05-30 10:00:00'),
('SZ007', 2, 'Content Performance', 'Python', 20, 30, 15000, 30, 40, 30, 25, 8, 90, 150, 50, '2024-04-28 09:00:00'),
('SZ007', 3, 'Recommendation Engine', 'Kafka', 24, 30, 50000, 10, 30, 60, 30, 20, 30, 300, 30, '2024-06-08 16:00:00'),
-- SZ008 workloads
('SZ008', 1, 'Sensor Data Analytics', 'Looker', 24, 30, 10000, 50, 35, 15, 20, 5, 60, 80, 40, '2024-05-18 11:00:00'),
('SZ008', 2, 'Predictive Maintenance', 'Power BI', 16, 25, 5000, 40, 40, 20, 15, 4, 90, 50, 60, '2024-04-12 10:00:00'),
-- SZ009 workloads
('SZ009', 1, 'Route Optimization', 'Tableau', 20, 30, 8000, 45, 35, 20, 20, 6, 60, 80, 55, '2024-05-22 13:00:00'),
('SZ009', 2, 'Fleet Analytics', 'Python', 16, 28, 6000, 50, 30, 20, 18, 5, 45, 60, 50, '2024-06-04 12:00:00'),
('SZ009', 3, 'Delivery Performance', 'Excel', 12, 30, 4000, 65, 25, 10, 15, 3, 30, 40, 70, '2024-04-30 15:00:00'),
-- SZ010 workloads
('SZ010', 1, 'Client Analytics Platform', 'Power BI', 24, 30, 12000, 40, 40, 20, 25, 8, 90, 100, 60, '2024-05-08 10:00:00'),
('SZ010', 2, 'Custom Reporting', 'Tableau', 20, 28, 8000, 50, 35, 15, 20, 6, 60, 80, 65, '2024-06-06 11:00:00'),
-- SZ011 workloads
('SZ011', 1, 'Sales Analytics', 'Looker', 14, 30, 3000, 60, 30, 10, 10, 3, 45, 30, 70, '2024-05-25 09:00:00'),
('SZ011', 2, 'Inventory Management', 'Excel', 10, 30, 2000, 70, 20, 10, 8, 2, 30, 20, 80, '2024-04-17 14:00:00'),
-- SZ012 workloads
('SZ012', 1, 'Trading Analytics', 'Jupyter', 24, 30, 30000, 20, 30, 50, 30, 15, 60, 250, 35, '2024-05-14 13:00:00'),
('SZ012', 2, 'Fraud Detection', 'Python', 24, 30, 40000, 10, 40, 50, 30, 20, 30, 300, 20, '2024-06-09 10:00:00'),
-- SZ013 workloads
('SZ013', 1, 'Student Performance', 'Tableau', 12, 30, 2500, 55, 30, 15, 10, 3, 60, 30, 65, '2024-05-02 11:00:00'),
('SZ013', 2, 'Course Analytics', 'R', 8, 25, 1500, 30, 50, 20, 8, 2, 90, 20, 50, '2024-04-10 10:00:00'),
-- SZ014 workloads
('SZ014', 1, 'Citizen Services', 'Tableau', 18, 30, 5000, 50, 35, 15, 15, 4, 60, 50, 60, '2024-05-27 12:00:00'),
('SZ014', 2, 'IoT Analytics', 'Power BI', 24, 30, 8000, 40, 40, 20, 20, 6, 90, 80, 50, '2024-06-07 13:00:00'),
('SZ014', 3, 'Urban Planning', 'Looker', 16, 28, 3000, 30, 50, 20, 12, 3, 120, 40, 70, '2024-04-19 09:00:00'),
-- SZ015 workloads
('SZ015', 1, 'Clinical Trial Analysis', 'SAS', 20, 30, 4000, 20, 50, 30, 15, 4, 120, 50, 55, '2024-05-16 10:00:00'),
('SZ015', 2, 'Drug Discovery Analytics', 'R', 16, 25, 3000, 10, 40, 50, 12, 3, 180, 40, 40, '2024-06-03 14:00:00'),
('SZ015', 3, 'Regulatory Compliance', 'Spotfire', 14, 30, 2500, 40, 40, 20, 10, 2, 60, 30, 70, '2024-04-14 11:00:00'),
-- SZ016 workloads
('SZ016', 1, 'Player Behavior Analytics', 'Power BI', 24, 30, 15000, 30, 35, 35, 25, 8, 60, 120, 45, '2024-05-19 13:00:00'),
('SZ016', 2, 'Live Operations', 'Looker', 24, 30, 20000, 40, 30, 30, 30, 10, 45, 150, 40, '2024-06-05 10:00:00'),
-- SZ017 workloads
('SZ017', 1, 'Manufacturing Analytics', 'Qlik', 20, 30, 6000, 45, 35, 20, 20, 5, 90, 60, 60, '2024-05-13 09:00:00'),
('SZ017', 2, 'Supply Chain Dashboard', 'SAP', 18, 30, 5000, 50, 30, 20, 18, 4, 60, 50, 65, '2024-04-21 10:00:00'),
('SZ017', 3, 'Quality Control Analytics', 'Qlik', 16, 28, 4000, 40, 40, 20, 15, 3, 120, 40, 70, '2024-06-02 11:00:00'),
-- SZ018 workloads
('SZ018', 1, 'Risk Assessment', 'SAS', 18, 30, 5000, 35, 45, 20, 18, 5, 90, 60, 55, '2024-05-29 10:00:00'),
('SZ018', 2, 'Claims Analytics', 'Tableau', 16, 30, 6000, 50, 35, 15, 20, 6, 60, 70, 65, '2024-04-13 09:00:00'),
('SZ018', 3, 'Actuarial Modeling', 'Excel', 12, 25, 2000, 20, 60, 20, 10, 2, 180, 25, 50, '2024-06-06 12:00:00'),
-- SZ019 workloads
('SZ019', 1, 'Trend Analysis', 'Looker', 14, 30, 3500, 45, 35, 20, 12, 4, 60, 35, 60, '2024-05-11 10:00:00'),
('SZ019', 2, 'Inventory Optimization', 'Power BI', 12, 28, 3000, 50, 30, 20, 10, 3, 45, 30, 65, '2024-06-04 13:00:00'),
-- SZ020 workloads
('SZ020', 1, 'Network Performance', 'MicroStrategy', 24, 30, 12000, 40, 40, 20, 25, 8, 90, 120, 55, '2024-05-21 11:00:00'),
('SZ020', 2, 'Customer Churn Analysis', 'Python', 20, 30, 10000, 30, 40, 30, 22, 6, 120, 100, 45, '2024-04-16 10:00:00'),
('SZ020', 3, 'Capacity Planning', 'Spark', 18, 28, 8000, 35, 35, 30, 20, 5, 60, 80, 50, '2024-06-08 15:00:00');

-- DATA_SOURCES TABLE INSERTS (50 rows total)

select * from SIZING_TOOL.CUSTOMER_SIZING.DATA_SOURCES;

INSERT INTO SIZING_TOOL.CUSTOMER_SIZING.DATA_SOURCES VALUES
-- SZ001 sources
('SZ001', 1, 'POS Transaction System', 'Oracle', 25.0, '2024-05-12 14:23:00'),
('SZ001', 2, 'E-commerce Platform', 'MySQL', 15.0, '2024-04-28 09:45:00'),
('SZ001', 3, 'Customer CRM', 'Salesforce', 8.0, '2024-06-01 16:10:00'),
-- SZ002 sources
('SZ002', 1, 'Trading Platform', 'SQL Server', 30.0, '2024-05-20 11:30:00'),
('SZ002', 2, 'Risk Management System', 'Oracle', 20.0, '2024-04-15 08:55:00'),
('SZ002', 3, 'Market Data Feed', 'Bloomberg API', 10.0, '2024-06-10 13:05:00'),
-- SZ003 sources
('SZ003', 1, 'Product Catalog', 'MongoDB', 12.0, '2024-05-05 10:00:00'),
('SZ003', 2, 'Order Management', 'MySQL', 18.0, '2024-04-22 15:40:00'),
('SZ003', 3, 'Customer Reviews', 'Elasticsearch', 5.0, '2024-06-08 12:20:00'),
-- SZ004 sources
('SZ004', 1, 'ML Training Data', 'S3', 10.0, '2024-05-18 17:15:00'),
('SZ004', 2, 'Model Registry', 'Postgres', 5.0, '2024-04-30 14:50:00'),
('SZ004', 3, 'Feature Store', 'Redis', 3.0, '2024-06-03 09:35:00'),
-- SZ005 sources
('SZ005', 1, 'Global ERP System', 'SAP', 200.0, '2024-05-25 13:00:00'),
('SZ005', 2, 'Store Operations', 'Teradata', 150.0, '2024-04-18 10:10:00'),
('SZ005', 3, 'Supply Chain', 'Oracle', 100.0, '2024-06-12 11:45:00'),
('SZ005', 4, 'Customer Loyalty', 'SQL Server', 50.0, '2024-05-02 16:30:00'),
-- SZ006 sources
('SZ006', 1, 'EMR System', 'SQL Server', 40.0, '2024-05-08 08:20:00'),
('SZ006', 2, 'Lab Results', 'Oracle', 30.0, '2024-04-25 13:55:00'),
('SZ006', 3, 'Billing System', 'SQL Server', 20.0, '2024-06-06 15:10:00'),
-- SZ007 sources
('SZ007', 1, 'Video Metadata', 'Cassandra', 80.0, '2024-05-15 12:40:00'),
('SZ007', 2, 'User Activity', 'Kafka', 120.0, '2024-04-12 09:25:00'),
('SZ007', 3, 'Content Library', 'S3', 60.0, '2024-06-04 18:00:00'),
-- SZ008 sources
('SZ008', 1, 'IoT Sensors', 'Cassandra', 30.0, '2024-05-28 11:15:00'),
('SZ008', 2, 'SCADA System', 'SQL Server', 20.0, '2024-04-20 10:50:00'),
-- SZ009 sources
('SZ009', 1, 'Fleet Management', 'Oracle', 35.0, '2024-05-10 14:05:00'),
('SZ009', 2, 'GPS Tracking', 'Dynamo DB', 25.0, '2024-04-27 16:30:00'),
('SZ009', 3, 'Order System', 'SQL Server', 15.0, '2024-06-09 13:20:00'),
-- SZ010 sources
('SZ010', 1, 'Client A Data', 'SQL Server', 5.0, '2024-05-03 09:00:00'),
('SZ010', 2, 'Client B Data', 'Oracle', 8.0, '2024-04-14 11:45:00'),
('SZ010', 3, 'Client C Data', 'Postgres', 10.0, '2024-06-11 17:10:00'),
-- SZ011 sources
('SZ011', 1, 'POS Systems', 'MySQL', 10.0, '2024-05-22 15:30:00'),
('SZ011', 2, 'Inventory Management', 'SQL Server', 8.0, '2024-04-19 13:20:00'),
-- SZ012 sources
('SZ012', 1, 'Trading Engine', 'Postgres', 50.0, '2024-05-13 10:10:00'),
('SZ012', 2, 'Market Data', 'Redis', 40.0, '2024-04-24 12:55:00'),
('SZ012', 3, 'User Accounts', 'MySQL', 20.0, '2024-06-07 14:40:00'),
-- SZ013 sources
('SZ013', 1, 'Student Information', 'Oracle', 12.0, '2024-05-06 11:25:00'),
('SZ013', 2, 'Learning Management', 'SQL Server', 8.0, '2024-04-29 16:15:00'),
-- SZ014 sources
('SZ014', 1, 'Citizen Services', 'Oracle', 60.0, '2024-05-30 13:50:00'),
('SZ014', 2, 'IoT Sensors', 'Postgres', 50.0, '2024-04-21 09:35:00'),
('SZ014', 3, 'GIS Data', 'Postgres', 40.0, '2024-06-05 12:55:00'),
-- SZ015 sources
('SZ015', 1, 'Clinical Trials', 'Oracle', 50.0, '2024-05-17 14:45:00'),
('SZ015', 2, 'Lab Systems', 'Mongo DB', 40.0, '2024-04-26 10:20:00'),
('SZ015', 3, 'Research Data', 'SQL Server', 30.0, '2024-06-02 15:30:00'),
-- SZ016 sources
('SZ016', 1, 'Game Events', 'Dynamo DB', 40.0, '2024-05-09 12:00:00'),
('SZ016', 2, 'Player Profiles', 'Mongo DB', 30.0, '2024-04-23 11:10:00'),
-- SZ017 sources
('SZ017', 1, 'Manufacturing ERP', 'SAP', 80.0, '2024-05-27 16:40:00'),
('SZ017', 2, 'Quality Systems', 'Oracle', 50.0, '2024-04-16 14:30:00'),
('SZ017', 3, 'Supply Chain', 'SQL Server', 40.0, '2024-06-13 10:25:00'),
-- SZ018 sources
('SZ018', 1, 'Policy Management', 'Guidewire', 45.0, '2024-05-11 13:15:00'),
('SZ018', 2, 'Claims System', 'SQL Server', 35.0, '2024-04-13 15:05:00'),
-- SZ019 sources
('SZ019', 1, 'E-commerce Platform', 'SQL Server', 20.0, '2024-05-01 09:50:00'),
('SZ019', 2, 'Inventory System', 'MySQL', 15.0, '2024-04-17 12:35:00'),
-- SZ020 sources
('SZ020', 1, 'Network Data', 'Oracle', 200.0, '2024-05-19 17:20:00'),
('SZ020', 2, 'Customer Billing', 'SQL Server', 150.0, '2024-04-11 08:40:00');

-- OTHER_WORKLOADS TABLE INSERTS (50 rows)

select * from SIZING_TOOL.CUSTOMER_SIZING.OTHER_WORKLOADS;

INSERT INTO SIZING_TOOL.CUSTOMER_SIZING.OTHER_WORKLOADS VALUES
-- SZ001 other workloads
('SZ001', 1, 'ETL Processing', 'Data Integration', 8, 30, 500, 1000.0, 10, 2, 120, 5, '2024-05-12 10:23:45'),
('SZ001', 2, 'ML Model Training', 'Machine Learning', 6, 20, 50, 500.0, 5, 1, 240, 2, '2024-04-28 14:11:32'),
('SZ001', 3, 'Data Quality Checks', 'Data Governance', 4, 30, 1000, 200.0, 15, 3, 60, 10, '2024-06-01 09:45:12'),
-- SZ002 other workloads
('SZ002', 1, 'Risk Calculations', 'Compute Intensive', 12, 30, 2000, 2000.0, 20, 5, 180, 20, '2024-05-20 16:05:00'),
('SZ002', 2, 'Compliance Reports', 'Reporting', 6, 20, 100, 500.0, 10, 2, 90, 5, '2024-04-15 08:30:00'),
-- SZ004 other workloads
('SZ004', 1, 'Feature Engineering', 'Data Science', 10, 25, 200, 300.0, 8, 3, 120, 5, '2024-05-30 13:22:10'),
('SZ004', 2, 'Model Deployment', 'ML Operations', 8, 30, 100, 200.0, 10, 2, 60, 3, '2024-06-05 11:10:00'),
('SZ004', 3, 'Data Validation', 'Data Quality', 4, 30, 500, 100.0, 15, 4, 30, 8, '2024-04-22 17:55:00'),
('SZ004', 4, 'API Services', 'Microservices', 24, 30, 5000, 50.0, 30, 10, 15, 50, '2024-05-18 19:40:00'),
-- SZ005 other workloads
('SZ005', 1, 'Global ETL', 'Data Integration', 24, 30, 1000, 5000.0, 30, 8, 240, 30, '2024-04-10 12:00:00'),
('SZ005', 2, 'Master Data Management', 'Data Governance', 16, 30, 500, 2000.0, 25, 5, 120, 15, '2024-05-25 15:15:00'),
('SZ005', 3, 'Real-time Streaming', 'Stream Processing', 24, 30, 10000, 3000.0, 30, 20, 60, 100, '2024-06-03 09:00:00'),
('SZ005', 4, 'Archive Processing', 'Batch Processing', 8, 30, 50, 8000.0, 5, 1, 480, 5, '2024-05-02 18:30:00'),
('SZ005', 5, 'Data Replication', 'Data Sync', 24, 30, 2000, 1500.0, 30, 10, 30, 50, '2024-04-18 07:45:00'),
-- SZ006 other workloads
('SZ006', 1, 'HIPAA Compliance Scans', 'Security', 12, 30, 200, 1000.0, 15, 3, 90, 10, '2024-05-08 10:10:00'),
('SZ006', 2, 'Patient Data Integration', 'ETL', 8, 30, 300, 1500.0, 20, 4, 120, 8, '2024-06-07 13:30:00'),
('SZ006', 3, 'Research Computing', 'Analytics', 6, 25, 100, 800.0, 10, 2, 180, 5, '2024-04-27 16:20:00'),
-- SZ007 other workloads
('SZ007', 1, 'Video Transcoding', 'Media Processing', 24, 30, 5000, 10000.0, 30, 15, 120, 200, '2024-05-14 09:00:00'),
('SZ007', 2, 'Recommendation Training', 'ML Pipeline', 12, 30, 50, 5000.0, 10, 2, 360, 10, '2024-06-02 11:11:00'),
('SZ007', 3, 'Content Indexing', 'Search', 16, 30, 1000, 2000.0, 20, 5, 60, 50, '2024-04-19 14:14:00'),
('SZ007', 4, 'CDN Cache Warming', 'Content Delivery', 24, 30, 2000, 3000.0, 30, 10, 30, 100, '2024-05-28 17:17:00'),
('SZ007', 5, 'User Segmentation', 'Analytics', 8, 30, 200, 1500.0, 15, 3, 90, 20, '2024-06-04 20:20:00'),
('SZ007', 6, 'A/B Testing Analysis', 'Experimentation', 12, 30, 500, 500.0, 20, 4, 60, 30, '2024-05-06 21:21:00'),
-- SZ008 other workloads
('SZ008', 1, 'Time Series Processing', 'IoT Analytics', 24, 30, 5000, 1500.0, 25, 8, 60, 80, '2024-04-30 08:08:00'),
('SZ008', 2, 'Anomaly Detection', 'ML Pipeline', 16, 30, 1000, 800.0, 20, 5, 90, 40, '2024-05-22 12:12:00'),
-- SZ009 other workloads
('SZ009', 1, 'Route Optimization', 'Optimization', 20, 30, 500, 1200.0, 25, 6, 120, 25, '2024-06-06 13:13:00'),
('SZ009', 2, 'GPS Data Processing', 'Stream Processing', 24, 30, 8000, 2000.0, 30, 15, 30, 150, '2024-05-16 15:15:00'),
('SZ009', 3, 'Delivery Predictions', 'ML Pipeline', 12, 28, 200, 600.0, 18, 4, 90, 15, '2024-04-25 17:17:00'),
('SZ009', 4, 'Customer Notifications', 'Event Processing', 24, 30, 10000, 100.0, 30, 20, 15, 200, '2024-05-10 19:19:00'),
-- SZ010 other workloads
('SZ010', 1, 'Multi-tenant ETL', 'Data Integration', 24, 30, 2000, 800.0, 25, 8, 90, 40, '2024-06-01 10:10:00'),
('SZ010', 2, 'Client Data Validation', 'Data Quality', 16, 30, 1500, 400.0, 20, 6, 60, 30, '2024-05-12 12:12:00'),
('SZ010', 3, 'Custom Report Generation', 'Reporting', 12, 28, 500, 300.0, 18, 4, 120, 20, '2024-04-20 14:14:00'),
('SZ010', 4, 'Data Archival', 'Storage Management', 4, 30, 50, 2000.0, 5, 1, 240, 5, '2024-05-24 16:16:00'),
('SZ010', 5, 'Security Auditing', 'Compliance', 8, 30, 300, 200.0, 10, 3, 60, 15, '2024-06-03 18:18:00'),
('SZ010', 6, 'Performance Monitoring', 'Operations', 24, 30, 5000, 100.0, 30, 15, 15, 100, '2024-04-28 20:20:00'),
('SZ010', 7, 'Backup Processing', 'Data Protection', 6, 30, 100, 1500.0, 10, 2, 180, 10, '2024-05-15 22:22:00'),
('SZ010', 8, 'Schema Migration', 'Database Ops', 2, 20, 20, 500.0, 5, 1, 240, 2, '2024-06-05 23:23:00'),
-- SZ012 other workloads
('SZ012', 1, 'Blockchain Processing', 'Crypto Operations', 24, 30, 10000, 2000.0, 30, 20, 60, 200, '2024-05-11 09:09:00'),
('SZ012', 2, 'Market Data Streaming', 'Real-time Data', 24, 30, 50000, 5000.0, 30, 30, 15, 500, '2024-06-06 11:11:00'),
('SZ012', 3, 'Fraud Detection ML', 'Security', 24, 30, 20000, 1000.0, 30, 15, 30, 300, '2024-04-29 13:13:00'),
-- SZ013 other workloads
('SZ013', 1, 'Grade Processing', 'Batch Processing', 4, 20, 100, 500.0, 10, 2, 120, 5, '2024-05-13 15:15:00'),
('SZ013', 2, 'Enrollment Analytics', 'Analytics', 6, 25, 200, 300.0, 15, 3, 90, 10, '2024-06-02 17:17:00'),
-- SZ014 other workloads
('SZ014', 1, 'IoT Data Ingestion', 'Stream Processing', 24, 30, 20000, 3000.0, 30, 15, 30, 300, '2024-04-21 19:19:00'),
('SZ014', 2, 'Citizen Portal Backend', 'Web Services', 24, 30, 10000, 500.0, 30, 20, 15, 200, '2024-05-23 21:21:00'),
('SZ014', 3, 'Emergency Response System', 'Real-time Processing', 24, 30, 5000, 1000.0, 30, 10, 60, 100, '2024-06-04 23:23:00'),
('SZ014', 4, 'Traffic Analysis', 'Analytics', 16, 30, 1000, 2000.0, 20, 5, 90, 50, '2024-05-17 08:08:00'),
('SZ014', 5, 'Public Data API', 'API Services', 24, 30, 15000, 200.0, 30, 25, 10, 400, '2024-04-26 10:10:00'),
-- SZ015 other workloads
('SZ015', 1, 'Clinical Data Processing', 'ETL', 12, 30, 400, 2500.0, 20, 4, 180, 20, '2024-05-19 12:12:00'),
('SZ015', 2, 'Genomic Analysis', 'Compute Intensive', 8, 25, 50, 5000.0, 10, 2, 480, 10, '2024-06-07 14:14:00'),
('SZ015', 3, 'Regulatory Submissions', 'Compliance', 6, 30, 100, 1000.0, 15, 3, 120, 8, '2024-04-23 16:16:00'),
('SZ015', 4, 'Lab Integration', 'Data Integration', 16, 30, 800, 1500.0, 25, 6, 60, 40, '2024-05-27 18:18:00'),
-- SZ016 other workloads
('SZ016', 1, 'Game Server Analytics', 'Real-time Processing', 24, 30, 30000, 3000.0, 30, 20, 30, 400, '2024-06-01 20:20:00'),
('SZ016', 2, 'Player Matching', 'Algorithm Processing', 24, 30, 20000, 500.0, 30, 15, 15, 300, '2024-05-21 22:22:00'),
('SZ016', 3, 'Event Processing', 'Stream Processing', 24, 30, 40000, 2000.0, 30, 25, 20, 500, '2024-04-24 09:09:00'),
('SZ016', 4, 'Leaderboard Updates', 'Cache Processing', 24, 30, 50000, 100.0, 30, 30, 10, 600, '2024-05-29 11:11:00'),
('SZ016', 5, 'Anti-cheat Analysis', 'Security', 24, 30, 10000, 1000.0, 30, 10, 60, 200, '2024-06-05 13:13:00'),
-- SZ017 other workloads
('SZ017', 1, 'Supply Chain ETL', 'Data Integration', 16, 30, 600, 3000.0, 25, 5, 180, 30, '2024-05-09 15:15:00'),
('SZ017', 2, 'Quality Predictions', 'ML Pipeline', 12, 28, 200, 1500.0, 20, 3, 120, 20, '2024-06-03 17:17:00'),
('SZ017', 3, 'Production Planning', 'Optimization', 8, 30, 300, 2000.0, 15, 2, 240, 15, '2024-04-29 19:19:00'),
('SZ017', 4, 'Sensor Data Processing', 'IoT Analytics', 24, 30, 8000, 2500.0, 30, 10, 45, 150, '2024-05-26 21:21:00'),
('SZ017', 5, 'Compliance Reporting', 'Reporting', 6, 30, 150, 1000.0, 10, 2, 90, 10, '2024-06-06 23:23:00'),
('SZ017', 6, 'Supplier Integration', 'B2B Integration', 20, 30, 1000, 800.0, 28, 8, 60, 80, '2024-05-13 08:08:00'),
-- SZ018 other workloads
('SZ018', 1, 'Actuarial Calculations', 'Compute Intensive', 12, 30, 300, 2000.0, 20, 4, 240, 25, '2024-04-18 10:10:00'),
('SZ018', 2, 'Claims Processing', 'Workflow Processing', 16, 30, 2000, 1500.0, 25, 6, 90, 60, '2024-05-31 12:12:00'),
('SZ018', 3, 'Risk Assessment ML', 'Machine Learning', 8, 28, 150, 1200.0, 15, 2, 180, 15, '2024-06-02 14:14:00'),
-- SZ019 other workloads
('SZ019', 1, 'Inventory Sync', 'Data Integration', 12, 30, 800, 600.0, 20, 4, 60, 20, '2024-05-16 16:16:00'),
('SZ019', 2, 'Price Optimization', 'Analytics', 8, 28, 300, 400.0, 15, 3, 90, 15, '2024-06-04 18:18:00'),
-- SZ020 other workloads
('SZ020', 1, 'Network Monitoring', 'Real-time Processing', 24, 30, 50000, 8000.0, 30, 25, 15, 800, '2024-04-22 20:20:00'),
('SZ020', 2, 'CDR Processing', 'Batch Processing', 24, 30, 2000, 10000.0, 30, 8, 240, 100, '2024-04-19 09:12:45'),
('SZ020', 3, 'Customer Analytics', 'Analytics', 16, 30, 1500, 3000.0, 25, 5, 120, 60, '2024-06-03 17:45:22'),
('SZ020', 4, 'Billing Calculations', 'Compute Intensive', 12, 30, 1000, 5000.0, 20, 4, 180, 50, '2024-05-10 11:08:37'),
('SZ020', 5, 'Network Optimization', 'ML Pipeline', 20, 30, 500, 2500.0, 28, 6, 150, 40, '2024-04-28 08:55:01'),
('SZ020', 6, 'Fraud Prevention', 'Security', 24, 30, 20000, 1500.0, 30, 15, 30, 300, '2024-06-07 20:31:55'),
('SZ020', 7, 'Service Quality Monitoring', 'Operations', 24, 30, 10000, 2000.0, 30, 10, 45, 200, '2024-05-15 13:17:29');

-- PIPELINES TABLE INSERTS (50 rows)
INSERT INTO SIZING_TOOL.CUSTOMER_SIZING.PIPELINES VALUES
-- SZ001 pipelines
('SZ001', 1, 'Sales Data Pipeline', 'Hourly', 24, 50.0, 30, 30, 4, 45, '2024-05-12 10:23:45'),
('SZ001', 2, 'Customer 360 Pipeline', 'Daily', 1, 200.0, 120, 30, 1, 120, '2024-04-28 14:12:11'),
('SZ001', 3, 'Inventory Update Pipeline', 'Real-time', 1440, 5.0, 5, 30, 20, 10, '2024-06-01 08:45:33'),
-- SZ002 pipelines
('SZ002', 1, 'Market Data Ingestion', 'Real-time', 2880, 10.0, 2, 30, 50, 5, '2024-05-30 16:01:22'),
('SZ002', 2, 'Risk Calculation Pipeline', 'Every 15 min', 96, 100.0, 45, 30, 8, 60, '2024-04-15 09:55:10'),
-- SZ003 pipelines
('SZ003', 1, 'Product Sync Pipeline', 'Every 30 min', 48, 25.0, 15, 30, 6, 20, '2024-05-18 13:40:00'),
('SZ003', 2, 'Order Processing Pipeline', 'Real-time', 5000, 2.0, 3, 30, 100, 5, '2024-06-05 11:22:19'),
-- SZ004 pipelines
('SZ004', 1, 'Training Data Pipeline', 'Daily', 1, 500.0, 180, 25, 1, 180, '2024-04-20 07:10:55'),
('SZ004', 2, 'Feature Store Update', 'Hourly', 24, 20.0, 20, 30, 3, 30, '2024-05-25 19:33:44'),
-- SZ005 pipelines
('SZ005', 1, 'Global Sales ETL', 'Every 4 hours', 6, 2000.0, 240, 30, 2, 240, '2024-05-02 12:00:00'),
('SZ005', 2, 'Store Inventory Pipeline', 'Every 15 min', 96, 150.0, 30, 30, 12, 45, '2024-06-08 15:15:15'),
('SZ005', 3, 'Supply Chain Update', 'Hourly', 24, 500.0, 60, 30, 6, 90, '2024-04-18 18:45:30'),
-- SZ006 pipelines
('SZ006', 1, 'Patient Data Integration', 'Every 30 min', 48, 75.0, 20, 30, 8, 30, '2024-05-10 09:09:09'),
('SZ006', 2, 'Lab Results Pipeline', 'Real-time', 1000, 5.0, 5, 30, 50, 10, '2024-06-03 21:30:00'),
-- SZ007 pipelines
('SZ007', 1, 'View Event Stream', 'Real-time', 10000, 50.0, 1, 30, 500, 2, '2024-05-28 17:17:17'),
('SZ007', 2, 'Content Metadata Update', 'Hourly', 24, 1000.0, 45, 30, 6, 60, '2024-04-22 20:20:20'),
('SZ007', 3, 'Recommendation Update', 'Every 6 hours', 4, 5000.0, 360, 30, 2, 360, '2024-06-06 06:06:06'),
-- SZ008 pipelines
('SZ008', 1, 'Sensor Data Collection', 'Every 5 min', 288, 20.0, 3, 30, 20, 5, '2024-05-14 11:11:11'),
('SZ008', 2, 'Predictive Model Update', 'Daily', 1, 1000.0, 180, 25, 1, 180, '2024-04-30 23:23:23'),
-- SZ009 pipelines
('SZ009', 1, 'GPS Tracking Pipeline', 'Real-time', 5000, 1.0, 1, 30, 200, 2, '2024-06-02 02:02:02'),
('SZ009', 2, 'Route Optimization Pipeline', 'Every 30 min', 48, 150.0, 30, 30, 8, 45, '2024-05-20 20:20:20'),
('SZ009', 3, 'Delivery Status Update', 'Every 10 min', 144, 25.0, 5, 30, 15, 10, '2024-04-25 05:05:05'),
-- SZ010 pipelines
('SZ010', 1, 'Client A Data Import', 'Daily', 1, 100.0, 60, 30, 1, 60, '2024-05-05 08:08:08'),
('SZ010', 2, 'Client B Data Import', 'Twice Daily', 2, 150.0, 90, 30, 1, 90, '2024-06-04 14:14:14'),
('SZ010', 3, 'Multi-tenant Report Gen', 'Hourly', 24, 50.0, 30, 30, 5, 45, '2024-04-16 16:16:16'),
-- SZ011 pipelines
('SZ011', 1, 'POS Data Sync', 'Every 15 min', 96, 10.0, 10, 30, 10, 15, '2024-05-22 22:22:22'),
('SZ011', 2, 'Inventory Update', 'Hourly', 24, 30.0, 20, 30, 4, 30, '2024-06-07 07:07:07'),
-- SZ012 pipelines
('SZ012', 1, 'Trade Processing Pipeline', 'Real-time', 20000, 5.0, 1, 30, 1000, 2, '2024-05-08 18:18:18'),
('SZ012', 2, 'Market Data Feed', 'Real-time', 50000, 1.0, 0.5, 30, 2000, 1, '2024-04-27 21:21:21'),
('SZ012', 3, 'Fraud Detection Pipeline', 'Real-time', 10000, 2.0, 2, 30, 500, 3, '2024-06-09 09:09:09'),
-- SZ013 pipelines
('SZ013', 1, 'Student Data Sync', 'Daily', 1, 200.0, 120, 25, 1, 120, '2024-05-16 12:12:12'),
('SZ013', 2, 'Grade Import Pipeline', 'Weekly', 0.14, 500.0, 180, 20, 1, 180, '2024-04-19 19:19:19'),
-- SZ014 pipelines
('SZ014', 1, 'IoT Sensor Pipeline', 'Real-time', 10000, 2.0, 1, 30, 500, 2, '2024-06-01 01:01:01'),
('SZ014', 2, 'Citizen Service Update', 'Every 10 min', 144, 50.0, 10, 30, 20, 15, '2024-05-13 13:13:13'),
('SZ014', 3, 'Traffic Data Pipeline', 'Every 5 min', 288, 100.0, 5, 30, 30, 8, '2024-04-21 21:21:21'),
-- SZ015 pipelines
('SZ015', 1, 'Clinical Trial Data', 'Daily', 1, 1500.0, 240, 30, 1, 240, '2024-05-07 07:07:07'),
('SZ015', 2, 'Lab Results Integration', 'Every 4 hours', 6, 500.0, 60, 30, 3, 90, '2024-06-03 03:03:03'),
('SZ015', 3, 'Research Data Pipeline', 'Weekly', 0.14, 3000.0, 360, 25, 1, 360, '2024-04-24 04:04:04'),
-- SZ016 pipelines
('SZ016', 1, 'Game Event Stream', 'Real-time', 30000, 10.0, 0.5, 30, 2000, 1, '2024-05-11 11:11:11'),
('SZ016', 2, 'Player Stats Update', 'Every 5 min', 288, 200.0, 5, 30, 50, 8, '2024-06-06 06:06:06'),
-- SZ017 pipelines
('SZ017', 1, 'Manufacturing Data ETL', 'Every 30 min', 48, 300.0, 30, 30, 10, 45, '2024-05-19 19:19:19'),
('SZ017', 2, 'Supply Chain Integration', 'Hourly', 24, 800.0, 60, 30, 6, 90, '2024-04-26 06:06:06'),
('SZ017', 3, 'Quality Metrics Pipeline', 'Every shift', 3, 1500.0, 120, 30, 1, 120, '2024-06-07 17:17:17'),
-- SZ018 pipelines
('SZ018', 1, 'Claims Processing ETL', 'Hourly', 24, 250.0, 45, 30, 6, 60, '2024-05-21 21:21:21'),
('SZ018', 2, 'Policy Update Pipeline', 'Daily', 1, 1000.0, 180, 30, 1, 180, '2024-04-29 09:09:09'),
-- SZ019 pipelines
('SZ019', 1, 'Product Catalog Sync', 'Every 4 hours', 6, 100.0, 30, 30, 2, 45, '2024-06-05 05:05:05'),
('SZ019', 2, 'Sales Data Pipeline', 'Hourly', 24, 50.0, 20, 30, 4, 30, '2024-05-15 15:15:15'),
-- SZ020 pipelines
('SZ020', 1, 'Network Data Collection', 'Every 5 min', 288, 500.0, 5, 30, 100, 8, '2024-04-23 23:23:23'),
('SZ020', 2, 'CDR Processing Pipeline', 'Every 15 min', 96, 2000.0, 30, 30, 20, 45, '2024-05-27 07:07:07'),
('SZ020', 3, 'Customer Usage Analytics', 'Hourly', 24, 1500.0, 60, 30, 8, 90, '2024-06-08 08:08:08');

/*--------------------------------------  Table Deletes ------------------------------------------------*/

Delete from sizing_main where sizing_id like 'SZ%';
Delete from pipelines where sizing_id like 'SZ%';
Delete from other_workloads where sizing_id like 'SZ%';
Delete from data_sources where sizing_id like 'SZ%';
Delete from analytics_workloads where sizing_id like 'SZ%';
