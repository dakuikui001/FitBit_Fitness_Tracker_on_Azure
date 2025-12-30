# FitBit Fitness Tracker Data Pipeline

A comprehensive data engineering project that processes FitBit fitness tracker data using Azure Databricks and Microsoft Fabric, implementing a medallion architecture (Bronze-Silver-Gold) for data transformation and analytics.

## Project Architecture

![Project Architecture](Project%20Architechture.png)

## [Power BI Dashboard]

![Power BI Dashboard](report/sample/Dashboard.png)

The project follows a modern data lakehouse architecture with the following components:

- **Azure Data Lake Storage (ADLS)**: Stores raw and processed data in different layers
- **Azure Databricks**: Performs data transformations using Spark Structured Streaming
- **Microsoft Fabric Lakehouse**: Provides analytics-ready data with shortcuts to ADLS
- **Microsoft Fabric Semantic Model**: Power BI semantic model for reporting
- **Power BI Reports**: Interactive dashboards for data visualization

## Overview

This project processes FitBit fitness data from multiple sources including:
- Calories (minute-level)
- Heart rate (second and minute-level)
- Steps (minute-level)
- Sleep (minute-level)
- Physical activity intensities (minute-level)
- METs (minute-level)
- Weight (daily)

The pipeline implements a medallion architecture pattern to progressively refine data quality and structure:

1. **Bronze Layer**: Raw data ingestion with basic cleaning
2. **Silver Layer**: Cleaned and aggregated data with business logic
3. **Gold Layer**: Unified, analytics-ready datasets

## Data Source

The dataset used in this project is sourced from Kaggle:

**FitBit Fitness Tracker Data**
- **Source**: [Kaggle Dataset - FitBit Fitness Tracker Data](https://www.kaggle.com/datasets/arashnic/fitbit)
- **Description**: A comprehensive dataset containing minute-level and daily-level fitness tracker data from FitBit devices
- **Format**: CSV files
- **License**: Please refer to the Kaggle dataset page for license information

The dataset includes various fitness metrics collected over a period of time from multiple users, providing a rich source of data for analytics and insights into user activity patterns, sleep quality, heart rate trends, and overall fitness metrics.

## Data Pipeline

### 1. Landing Zone (Raw Data)

Raw CSV files from the Kaggle FitBit dataset are ingested into Azure Data Lake Storage landing zone:
- Source: [Kaggle FitBit Dataset](https://www.kaggle.com/datasets/arashnic/fitbit)
- Location: `fitbit-landing-dev/landing_zone/`
- Format: CSV files with headers
- Files are monitored using Auto Loader (CloudFiles)

### 2. Bronze Layer (Raw Ingestion)

**Purpose**: Ingest raw data from landing zone with minimal transformations

**Location**: `fitbit-medallion-dev/bronze/`

**Process**:
- Streams data from landing zone using Spark Structured Streaming
- Applies basic preprocessing:
  - Duplicate removal
  - Null value handling (fills with 'Unknown' for strings, 0 for numerics)
  - All-null row removal
- Adds metadata columns:
  - `load_time`: Timestamp when data was loaded
  - `source_file`: Path to source file
  - `timeKey`: Time component (HH:mm:ss format)

**Tables Created**:
- `calories_min_bz`: Minute-level calorie data
- `heartrate_sec_bz`: Second-level heart rate data
- `intensities_min_bz`: Minute-level activity intensity data
- `METs_min_bz`: Minute-level METs (Metabolic Equivalent of Task) data
- `sleep_min_bz`: Minute-level sleep data
- `steps_min_bz`: Minute-level step count data
- `weight_daily_bz`: Daily weight measurements

**Implementation**: `databricks/FitBit_Fitness_Tracker_project/04_bronze.ipynb`

### 3. Silver Layer (Cleaned & Aggregated)

**Purpose**: Clean, aggregate, and enrich data for analytics

**Location**: `fitbit-medallion-dev/silver/`

**Process**:
- Reads from Bronze layer using Delta Streaming
- Applies aggregations and business logic
- Uses MERGE operations for upsert logic (handles updates and new records)
- Implements watermarking for late-arriving data

**Tables Created**:

**Daily Aggregations**:
- `calories_daily_sl`: Daily total calories per user
- `heartrate_daily_sl`: Daily average and max heart rate per user
- `intensities_daily_sl`: Daily activity minutes by intensity level:
  - Sedentary minutes (intensity = 0)
  - Lightly active minutes (intensity = 1)
  - Fairly active minutes (intensity = 2)
  - Very active minutes (intensity = 3)
- `sleep_daily_sl`: Daily sleep metrics (asleep, restless, awake, total bed time)
- `steps_daily_sl`: Daily total steps per user

**Minute-Level Aggregations**:
- `heartrate_min_sl`: Minute-level average and max heart rate (aggregated from second-level data)

**Lookup Tables**:
- `user_list`: Distinct list of users
- `date_list`: Distinct list of dates with data

**Implementation**: `databricks/FitBit_Fitness_Tracker_project/05_silver.ipynb`

### 4. Gold Layer (Analytics-Ready)

**Purpose**: Create unified, business-ready datasets for analytics and reporting

**Location**: `fitbit-medallion-dev/gold/`

**Process**:
- Combines multiple Silver layer tables into unified fact table
- Uses full outer joins to ensure complete user-date combinations
- Handles missing data with COALESCE (defaults to 0)
- Creates user-date grid for comprehensive coverage

**Tables Created**:
- `activity_daily_gold`: Unified daily activity metrics including:
  - Total steps
  - Total calories
  - Activity minutes (very active, fairly active, lightly active, sedentary)
  - Heart rate (average and max)
  - Sleep metrics (asleep minutes, total bed time)

**Implementation**: `databricks/FitBit_Fitness_Tracker_project/06_gold.ipynb`

### 5. Microsoft Fabric Integration

**Lakehouse**: 
- Creates shortcuts to ADLS Delta tables
- Provides unified access to Bronze, Silver, and Gold layers
- Location: `Fabric/LH_fitbit.Lakehouse/`

**Semantic Model**:
- Power BI semantic model built on Lakehouse data
- Implements relationships between tables
- Includes calculated measures and hierarchies
- Location: `Fabric/fitbit_model.SemanticModel/`

**Power BI Report**:
- Interactive dashboards for fitness analytics
- Visualizes key metrics and trends
- Location: `Fabric/fitbit_analysis_report.Report/`


## Project Structure

```
Azure_git/
├── adls/                          # Azure Data Lake Storage structure
│   ├── fitbit-landing-dev/       # Landing zone for raw CSV files
│   ├── fitbit-medallion-dev/     # Medallion architecture layers
│   │   ├── bronze/               # Bronze layer (raw data)
│   │   ├── silver/               # Silver layer (cleaned & aggregated)
│   │   ├── gold/                 # Gold layer (analytics-ready)
│   │   └── initial/              # Lookup tables (date_lookup, user_list, date_list)
│   └── fitbit-checkpoints-dev/   # Spark streaming checkpoints
│
├── databricks/                    # Databricks notebooks
│   └── FitBit_Fitness_Tracker_project/
│       ├── 00_main.ipynb         # Main orchestration notebook
│       ├── 01_config.ipynb       # Configuration and helper functions
│       ├── 02_setup.ipynb        # Database and table setup
│       ├── 03_history_loader.ipynb  # Load historical/lookup data
│       ├── 04_bronze.ipynb       # Bronze layer ingestion
│       ├── 05_silver.ipynb       # Silver layer transformations
│       ├── 06_gold.ipynb         # Gold layer aggregations
│       └── 07_run.ipynb          # Production run notebook
│
├── Fabric/                        # Microsoft Fabric components
│   ├── LH_fitbit.Lakehouse/      # Fabric Lakehouse with ADLS shortcuts
│   ├── fitbit_model.SemanticModel/  # Power BI semantic model
│   └── fitbit_analysis_report.Report/  # Power BI report
│
└── report/                        # Reports and dashboards
    ├── fitbit_analysis_report.pbix  # Power BI desktop file
    └── sample/
        └── Dashboard.png         # Dashboard screenshot
```

## Data Flow

```
CSV Files (FitBit Export)
    ↓
Landing Zone (ADLS)
    ↓
Bronze Layer (Raw Ingestion + Basic Cleaning)
    ↓
Silver Layer (Aggregation + Business Logic)
    ↓
Gold Layer (Unified Analytics Dataset)
    ↓
Fabric Lakehouse (Shortcuts to ADLS)
    ↓
Fabric Semantic Model
    ↓
Power BI Reports
```

## Key Features

### Streaming Processing
- Uses Spark Structured Streaming for real-time data processing
- Supports both batch (`once=True`) and continuous streaming modes
- Implements checkpointing for fault tolerance
- Uses watermarking for handling late-arriving data

### Data Quality
- Duplicate detection and removal
- Null value handling with appropriate defaults
- Schema enforcement at ingestion
- Metadata tracking (load_time, source_file)

### Scalability
- Delta Lake format for ACID transactions
- Partitioned tables by date
- Optimized write and auto-compaction enabled
- Resource pools for workload management

### Environment Support
- Multi-environment support (dev, uat, prod)
- Environment-specific catalogs and configurations
- Easy deployment across environments

## Getting Started

### Prerequisites

- Azure Databricks workspace
- Azure Data Lake Storage Gen2 account
- Microsoft Fabric workspace (for reporting)
- Access to FitBit data exports (CSV format)

### Setup Steps

1. **Configure External Locations** in Databricks:
   - `fitbit_landing_dev`: Points to landing zone
   - `fitbit_medallion_dev`: Points to medallion layers
   - `fitbit_checkpoints_dev`: Points to checkpoint directory

2. **Run Setup Notebook** (`02_setup.ipynb`):
   - Creates catalog and database
   - Creates all Delta tables with proper schemas

3. **Load Historical Data** (`03_history_loader.ipynb`):
   - Generates date lookup table (2010-2030)
   - Creates initial date and user lists

4. **Start Data Ingestion**:
   - Copy CSV files to landing zone
   - Run Bronze layer notebook (`04_bronze.ipynb`)
   - Run Silver layer notebook (`05_silver.ipynb`)
   - Run Gold layer notebook (`06_gold.ipynb`)

5. **Set Up Fabric**:
   - Create Lakehouse shortcuts to ADLS
   - Create semantic model from Lakehouse
   - Build Power BI reports

### Running the Pipeline

#### One-Time Batch Run
```python
env = "dev"
once = True
processing_time = "5 seconds"
```

#### Continuous Streaming
```python
env = "dev"
once = False
processing_time = "5 seconds"  # Micro-batch interval
```

Use `07_run.ipynb` for production runs with proper configuration.

## Data Schemas

### Bronze Layer Schemas

All bronze tables include:
- User ID and activity timestamp
- Metric-specific columns
- Date column
- `timeKey` (HH:mm:ss format)
- `load_time` (ingestion timestamp)
- `source_file` (source file path)

### Silver Layer Schemas

**Daily Aggregations**: User ID, Date, Aggregated Metrics

**Minute Aggregations**: User ID, Activity Minute, Aggregated Metrics, Date, TimeKey

### Gold Layer Schema

**activity_daily_gold**:
- `user_id`: Long
- `date`: Date
- `total_steps`: Long
- `total_calories`: Long
- `very_active_minutes`: Long
- `fairly_active_minutes`: Long
- `lightly_active_minutes`: Long
- `sedentary_minutes`: Long
- `avg_heartrate`: Double
- `max_heartrate`: Double
- `asleep_minutes`: Long
- `total_minutes_in_bed`: Long

## Technologies Used

- **Azure Databricks**: Data processing engine
- **Apache Spark**: Distributed processing framework
- **Delta Lake**: ACID transactions and time travel
- **Structured Streaming**: Real-time data processing
- **Azure Data Lake Storage Gen2**: Data storage
- **Microsoft Fabric**: Analytics and reporting platform
- **Power BI**: Data visualization
- **Python/PySpark**: Programming language

## Architecture Patterns

### Medallion Architecture
- **Bronze**: Raw data as-is
- **Silver**: Cleaned and validated data
- **Gold**: Business-level aggregations

### Streaming Architecture
- **Source**: ADLS landing zone (Auto Loader)
- **Processing**: Spark Structured Streaming
- **Sink**: Delta Lake tables
- **Mode**: Append (Bronze), Update (Silver/Gold)

### Data Quality
- Schema enforcement
- Duplicate handling
- Null value strategies
- Metadata tracking

## Monitoring & Maintenance

- Checkpoint locations track streaming progress
- Delta Lake provides transaction logs for audit
- Load time and source file columns enable data lineage
- Use Databricks SQL or Spark SQL to query processed data

## Future Enhancements

- Add data quality validation rules
- Implement data retention policies
- Add alerting for pipeline failures
- Enhance Power BI reports with additional metrics
- Add data quality dashboards

