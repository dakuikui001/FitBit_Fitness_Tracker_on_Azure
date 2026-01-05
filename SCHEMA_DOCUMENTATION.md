# Database Schema Documentation

This document provides a comprehensive schema reference for all data tables in the FitBit Fitness Tracker Data Pipeline project.

## Table of Contents

### Bronze Layer Tables
1. [calories_min_bz](#1-calories_min_bz)
2. [heartrate_sec_bz](#2-heartrate_sec_bz)
3. [intensities_min_bz](#3-intensities_min_bz)
4. [METs_min_bz](#4-mets_min_bz)
5. [sleep_min_bz](#5-sleep_min_bz)
6. [steps_min_bz](#6-steps_min_bz)
7. [weight_daily_bz](#7-weight_daily_bz)

### Silver Layer Tables
8. [calories_daily_sl](#8-calories_daily_sl)
9. [heartrate_min_sl](#9-heartrate_min_sl)
10. [heartrate_daily_sl](#10-heartrate_daily_sl)
11. [intensities_daily_sl](#11-intensities_daily_sl)
12. [sleep_daily_sl](#12-sleep_daily_sl)
13. [steps_daily_sl](#13-steps_daily_sl)
14. [user_list](#14-user_list)
15. [date_list](#15-date_list)

### Gold Layer Tables
16. [activity_daily_gold](#16-activity_daily_gold)

### Lookup Tables
17. [date_lookup](#17-date_lookup)

### Data Quality Tables
18. [data_quality_quarantine](#18-data_quality_quarantine)

---

## Bronze Layer Tables

The Bronze layer contains raw ingested data with minimal transformations. All Bronze tables include metadata columns for tracking data lineage and ingestion timing.

### 1. calories_min_bz

**Description**: Raw minute-level calorie consumption data from FitBit devices.

**Location**: `adls/medallion/bronze/calories_min/`

| Column Name | Data Type | Description |
|------------|-----------|-------------|
| user_id | long | Unique identifier for the FitBit user |
| activity_minute | timestamp | Timestamp of the minute when calories were recorded |
| calories | double | Number of calories burned during the minute |
| date | date | Date of the activity (derived from activity_minute) |
| timeKey | string | Time-based partitioning key for efficient querying |
| load_time | timestamp | Timestamp when the record was ingested into the pipeline |
| source_file | string | Path to the source CSV file from which this record was loaded |

**Notes**: 
- Data validation: calories ≥ 0
- Source: Landing zone CSV files
- Processed via Spark Structured Streaming with Auto Loader

---

### 2. heartrate_sec_bz

**Description**: Raw second-level heart rate measurements from FitBit devices.

**Location**: `adls/medallion/bronze/heartrate_sec/`

| Column Name | Data Type | Description |
|------------|-----------|-------------|
| user_id | long | Unique identifier for the FitBit user |
| time | timestamp | Timestamp of the second when heart rate was measured |
| value | long | Heart rate value in beats per minute (BPM) |
| date | date | Date of the measurement (derived from time) |
| timeKey | string | Time-based partitioning key for efficient querying |
| load_time | timestamp | Timestamp when the record was ingested into the pipeline |
| source_file | string | Path to the source CSV file from which this record was loaded |

**Notes**:
- Data validation: heart rate value between 0-200 BPM
- Highest granularity heart rate data (second-level)
- Source: Landing zone CSV files

---

### 3. intensities_min_bz

**Description**: Raw minute-level activity intensity data from FitBit devices.

**Location**: `adls/medallion/bronze/intensities_min/`

| Column Name | Data Type | Description |
|------------|-----------|-------------|
| user_id | long | Unique identifier for the FitBit user |
| activity_minute | timestamp | Timestamp of the minute when intensity was recorded |
| intensity | long | Activity intensity level (0=sedentary, 1=lightly active, 2=fairly active, 3=very active) |
| date | date | Date of the activity (derived from activity_minute) |
| timeKey | string | Time-based partitioning key for efficient querying |
| load_time | timestamp | Timestamp when the record was ingested into the pipeline |
| source_file | string | Path to the source CSV file from which this record was loaded |

**Notes**:
- Data validation: intensity value between 0-3
- Intensity levels map to activity categories: sedentary, lightly active, fairly active, very active
- Source: Landing zone CSV files

---

### 4. METs_min_bz

**Description**: Raw minute-level Metabolic Equivalent of Task (METs) data from FitBit devices.

**Location**: `adls/medallion/bronze/METs_min/`

| Column Name | Data Type | Description |
|------------|-----------|-------------|
| user_id | long | Unique identifier for the FitBit user |
| activity_minute | timestamp | Timestamp of the minute when METs were recorded |
| mets | long | Metabolic Equivalent of Task value (measure of energy expenditure) |
| date | date | Date of the activity (derived from activity_minute) |
| timeKey | string | Time-based partitioning key for efficient querying |
| load_time | timestamp | Timestamp when the record was ingested into the pipeline |
| source_file | string | Path to the source CSV file from which this record was loaded |

**Notes**:
- Data validation: METs value between 10-200
- METs represent the ratio of work metabolic rate to resting metabolic rate
- Source: Landing zone CSV files

---

### 5. sleep_min_bz

**Description**: Raw minute-level sleep data from FitBit devices.

**Location**: `adls/medallion/bronze/sleep_min/`

| Column Name | Data Type | Description |
|------------|-----------|-------------|
| user_id | long | Unique identifier for the FitBit user |
| activity_minute | timestamp | Timestamp of the minute when sleep state was recorded |
| value | long | Sleep state value (1=asleep, 2=restless, 3=awake) |
| log_id | long | Identifier linking sleep records to a specific sleep session |
| date | date | Date of the sleep record (derived from activity_minute) |
| timeKey | string | Time-based partitioning key for efficient querying |
| load_time | timestamp | Timestamp when the record was ingested into the pipeline |
| source_file | string | Path to the source CSV file from which this record was loaded |

**Notes**:
- Data validation: sleep value between 1-3
- Multiple records share the same log_id when they belong to the same sleep session
- Source: Landing zone CSV files

---

### 6. steps_min_bz

**Description**: Raw minute-level step count data from FitBit devices.

**Location**: `adls/medallion/bronze/steps_min/`

| Column Name | Data Type | Description |
|------------|-----------|-------------|
| user_id | long | Unique identifier for the FitBit user |
| activity_minute | timestamp | Timestamp of the minute when steps were recorded |
| steps | long | Number of steps taken during the minute |
| date | date | Date of the activity (derived from activity_minute) |
| timeKey | string | Time-based partitioning key for efficient querying |
| load_time | timestamp | Timestamp when the record was ingested into the pipeline |
| source_file | string | Path to the source CSV file from which this record was loaded |

**Notes**:
- Data validation: steps ≥ 0
- Source: Landing zone CSV files

---

### 7. weight_daily_bz

**Description**: Raw daily weight and body composition measurements from FitBit devices.

**Location**: `adls/medallion/bronze/weight_daily/`

| Column Name | Data Type | Description |
|------------|-----------|-------------|
| user_id | long | Unique identifier for the FitBit user |
| date | date | Date of the weight measurement |
| weight_kg | double | Weight in kilograms |
| weight_pounds | double | Weight in pounds |
| fat | double | Body fat percentage |
| bmi | double | Body Mass Index (BMI) |
| is_manual_report | boolean | Indicates if the measurement was manually entered by the user |
| log_id | long | Identifier for the weight log entry |
| activity_minute | timestamp | Timestamp of when the weight was recorded |
| load_time | timestamp | Timestamp when the record was ingested into the pipeline |
| source_file | string | Path to the source CSV file from which this record was loaded |

**Notes**:
- Data validation: weight_kg ≥ 0, weight_pounds ≥ 0, fat ≥ 0, bmi ≥ 0
- Daily-level data (not minute-level like other Bronze tables)
- Source: Landing zone CSV files

---

## Silver Layer Tables

The Silver layer contains cleaned and aggregated data with business logic applied. Data is read from Bronze layer using Delta Streaming and processed with MERGE operations for upsert logic.

### 8. calories_daily_sl

**Description**: Daily aggregated calorie consumption data.

**Location**: `adls/medallion/silver/calories_daily/`

| Column Name | Data Type | Description |
|------------|-----------|-------------|
| user_id | long | Unique identifier for the FitBit user |
| daily_calories | double | Total calories burned for the day (sum of minute-level calories) |
| date | date | Date of the activity |

**Notes**:
- Aggregated from `calories_min_bz` table
- Contains one record per user per day
- Used for daily analytics and reporting

---

### 9. heartrate_min_sl

**Description**: Minute-level aggregated heart rate data with statistics.

**Location**: `adls/medallion/silver/heartrate_min/`

| Column Name | Data Type | Description |
|------------|-----------|-------------|
| user_id | long | Unique identifier for the FitBit user |
| activity_minute | timestamp | Timestamp of the minute when heart rate was measured |
| avg_heartrate | double | Average heart rate during the minute (aggregated from second-level data) |
| max_heartrate | double | Maximum heart rate during the minute |
| date | date | Date of the measurement (derived from activity_minute) |
| timeKey | string | Time-based partitioning key for efficient querying |

**Notes**:
- Aggregated from `heartrate_sec_bz` table
- Converts second-level data to minute-level with statistics
- Contains average and maximum heart rate per minute

---

### 10. heartrate_daily_sl

**Description**: Daily aggregated heart rate statistics.

**Location**: `adls/medallion/silver/heartrate_daily/`

| Column Name | Data Type | Description |
|------------|-----------|-------------|
| user_id | long | Unique identifier for the FitBit user |
| avg_heartrate | double | Average heart rate for the day |
| max_heartrate | double | Maximum heart rate for the day |
| date | date | Date of the measurement |

**Notes**:
- Aggregated from `heartrate_min_sl` or `heartrate_sec_bz` table
- Contains one record per user per day
- Used for daily analytics and reporting

---

### 11. intensities_daily_sl

**Description**: Daily aggregated activity intensity data broken down by intensity level.

**Location**: `adls/medallion/silver/intensities_daily/`

| Column Name | Data Type | Description |
|------------|-----------|-------------|
| user_id | long | Unique identifier for the FitBit user |
| sedentary_minutes | double | Total minutes spent in sedentary activity (intensity = 0) |
| lightly_active_minutes | double | Total minutes spent in lightly active activity (intensity = 1) |
| fairly_active_minutes | double | Total minutes spent in fairly active activity (intensity = 2) |
| very_active_minutes | double | Total minutes spent in very active activity (intensity = 3) |
| date | date | Date of the activity |

**Notes**:
- Aggregated from `intensities_min_bz` table
- Converts minute-level intensity values into daily totals by category
- Contains one record per user per day
- Used for daily analytics and reporting

---

### 12. sleep_daily_sl

**Description**: Daily aggregated sleep data with breakdown by sleep state.

**Location**: `adls/medallion/silver/sleep_daily/`

| Column Name | Data Type | Description |
|------------|-----------|-------------|
| user_id | long | Unique identifier for the FitBit user |
| total_minutes_in_bed | double | Total minutes the user was in bed (sum of all sleep states) |
| asleep_minutes | double | Total minutes in asleep state (value = 1) |
| Restless_minuts | double | Total minutes in restless state (value = 2) (Note: typo in column name preserved) |
| awake_minutes | double | Total minutes in awake state (value = 3) |
| log_id | long | Identifier for the sleep log entry |
| date | date | Date of the sleep record |

**Notes**:
- Aggregated from `sleep_min_bz` table
- Groups minute-level sleep data by log_id and date
- Contains one record per sleep session per user
- Used for sleep analytics and reporting

---

### 13. steps_daily_sl

**Description**: Daily aggregated step count data.

**Location**: `adls/medallion/silver/steps_daily/`

| Column Name | Data Type | Description |
|------------|-----------|-------------|
| user_id | long | Unique identifier for the FitBit user |
| total_steps | long | Total number of steps taken during the day (sum of minute-level steps) |
| date | date | Date of the activity |

**Notes**:
- Aggregated from `steps_min_bz` table
- Contains one record per user per day
- Used for daily analytics and reporting

---

### 14. user_list

**Description**: Lookup table containing all unique user identifiers in the system.

**Location**: `adls/medallion/initial/user_list/`

| Column Name | Data Type | Description |
|------------|-----------|-------------|
| user_id | long | Unique identifier for the FitBit user (Primary Key) |

**Notes**:
- Reference/lookup table
- Contains distinct user IDs from all data sources
- Used for creating user-date grids and joins
- Maintained in the initial/medallion layer

---

### 15. date_list

**Description**: Lookup table containing all unique dates in the system.

**Location**: `adls/medallion/initial/date_list/`

| Column Name | Data Type | Description |
|------------|-----------|-------------|
| date | date | Calendar date (Primary Key) |

**Notes**:
- Reference/lookup table
- Contains distinct dates from all data sources
- Used for creating user-date grids and joins
- Maintained in the initial/medallion layer

---

## Gold Layer Tables

The Gold layer contains unified, analytics-ready datasets that combine multiple Silver layer tables for business intelligence and reporting.

### 16. activity_daily_gold

**Description**: Unified daily activity metrics combining data from multiple Silver layer tables.

**Location**: `adls/medallion/gold/activity_daily/`

| Column Name | Data Type | Description |
|------------|-----------|-------------|
| user_id | long | Unique identifier for the FitBit user |
| date | date | Date of the activity |
| total_steps | long | Total number of steps taken during the day (from steps_daily_sl) |
| total_calories | long | Total calories burned during the day (from calories_daily_sl) |
| very_active_minutes | long | Total minutes in very active intensity (from intensities_daily_sl) |
| fairly_active_minutes | long | Total minutes in fairly active intensity (from intensities_daily_sl) |
| lightly_active_minutes | long | Total minutes in lightly active intensity (from intensities_daily_sl) |
| sedentary_minutes | long | Total minutes in sedentary intensity (from intensities_daily_sl) |
| avg_heartrate | double | Average heart rate for the day (from heartrate_daily_sl) |
| max_heartrate | double | Maximum heart rate for the day (from heartrate_daily_sl) |
| asleep_minutes | long | Total minutes in asleep state (from sleep_daily_sl) |
| total_minutes_in_bed | long | Total minutes in bed (from sleep_daily_sl) |

**Notes**:
- Fact table combining multiple Silver layer tables
- Primary table for analytics and reporting
- Contains one record per user per day
- Used by Power BI reports and semantic models
- Created using foreachBatch for micro-batch processing

---

## Lookup Tables

Lookup tables provide reference data and dimensional information for data analysis.

### 17. date_lookup

**Description**: Enhanced date dimension table with derived date attributes for time-based analytics.

**Location**: `adls/medallion/initial/date_lookup/`

| Column Name | Data Type | Description |
|------------|-----------|-------------|
| date | date | Calendar date (Primary Key) |
| week | int | Week number of the year (1-53) |
| year | int | Year (e.g., 2016) |
| month | int | Month of the year (1-12) |
| dayofweek | int | Day of the week (1=Sunday, 2=Monday, ..., 7=Saturday) |
| dayofmonth | int | Day of the month (1-31) |
| dayofyear | int | Day of the year (1-366) |
| week_part | string | Weekday/weekend indicator or week part classification |

**Notes**:
- Date dimension table for time-based analytics
- Generated from date_list with additional derived attributes
- Used for time intelligence and date-based filtering in reports
- Supports Power BI date hierarchies and time intelligence functions

---

## Data Quality Tables

Data quality tables store records that fail validation rules during data ingestion.

### 18. data_quality_quarantine

**Description**: Universal quarantine table for storing records that failed Great Expectations (GX) validation during Bronze layer ingestion.

**Location**: `adls/gx/data_quality_quarantine/`

| Column Name | Data Type | Description |
|------------|-----------|-------------|
| table_name | string | The name of the source table where the data originated (e.g., 'calories_min_bz') |
| gx_batch_id | string | The identifier for the GX validation run (casted to string) |
| violated_rules | string | A list or description of the rules that failed validation |
| raw_data | string | The original record stored in JSON format |
| ingestion_time | timestamp | The timestamp when the record was quarantined |

**Notes**:
- Stores records that fail Great Expectations validation rules
- Used for data quality monitoring and troubleshooting
- Records are stored as JSON strings in raw_data column
- Part of the data quality framework using Great Expectations
- Quarantined data can be analyzed and reprocessed after fixing issues
- Validation rules include schema validation, non-null checks, and value range validation

---

## Schema Notes

### Data Types Reference

- **long**: 64-bit signed integer
- **double**: 64-bit floating-point number
- **string**: Variable-length character string
- **date**: Date value (year, month, day)
- **timestamp**: Date and time value with timezone
- **boolean**: True/false value

### Common Patterns

1. **Metadata Columns**: All Bronze layer tables include `load_time` and `source_file` columns for data lineage tracking.

2. **Time Keys**: Most time-series tables include `timeKey` column for efficient partitioning and querying.

3. **Primary Keys**: 
   - Most tables use composite keys of (user_id, date) or (user_id, activity_minute)
   - Lookup tables (user_list, date_list) use single-column primary keys

4. **Data Flow**: 
   - Landing Zone → Bronze (raw ingestion)
   - Bronze → Silver (cleaned & aggregated)
   - Silver → Gold (unified analytics-ready)

5. **Naming Conventions**:
   - Bronze tables: `{metric}_{granularity}_bz` (e.g., `calories_min_bz`)
   - Silver tables: `{metric}_{granularity}_sl` (e.g., `calories_daily_sl`)
   - Gold tables: `{purpose}_gold` (e.g., `activity_daily_gold`)

---

## Additional Resources

- **Project README**: See `README.md` for project overview and architecture
- **Setup Scripts**: Table creation scripts are in `databricks/02_setup.ipynb`
- **Data Quality**: Great Expectations configuration in `databricks/great_expectations_setting.ipynb`
- **Semantic Model**: Power BI semantic model definitions in `fabric/fitbit_model.SemanticModel/`

---

*Schema Version: 1.0*

