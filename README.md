# HR Workforce Analytics Lakehouse

This project is an end-to-end Data Engineering pipeline built using Spark, Delta Lake, MinIO, DuckDB, and Streamlit.

The goal of the project was to simulate a modern Lakehouse architecture using the Oracle HR schema and build analytical KPI dashboards on top of it.

---

# What We Built

We extracted HR data from Oracle and implemented a Medallion Architecture:

```text
Oracle HR Schema
        ↓
Raw Parquet Landing
        ↓
Bronze Layer (Delta Tables)
        ↓
Silver Layer (Cleaned + Enriched Data)
        ↓
Gold Layer (Business KPIs)
        ↓
DuckDB + Streamlit Dashboard
```

---

# Technologies Used

- Apache Spark
- Delta Lake
- MinIO (S3-compatible object storage)
- OracleDB
- DuckDB
- Streamlit
- Docker
- PySpark
- Pandas

---

# Project Features

## Data Ingestion
- Extracted tables from Oracle HR schema
- Stored raw parquet files in MinIO buckets
- Added ingestion metadata and batch information

## Bronze Layer
- Converted raw parquet files into Delta tables
- Implemented schema overwrite handling
- Preserved ingestion history

## Silver Layer
Performed:
- data cleaning
- joins
- feature engineering
- analytical modeling
- metadata lineage

### Silver Tables
- `employees_enriched`
- `employee_hierarchy`
- `employee_tenure_analytics`

## Gold Layer
Built analytical KPI tables for:
- workforce analysis
- compensation analysis
- hiring trends

### Gold Tables
- `workforce_summary`
- `compensation_summary`
- `hiring_trends`

---

# Concepts Covered

- Medallion Architecture
- Delta Lake
- Object Storage Lakehouse
- Batch Processing
- Metadata Lineage
- Schema Evolution
- Feature Engineering
- Window Functions
- Partitioning
- Partition Pruning
- Hierarchical Self Joins
- KPI Aggregation
- Dockerized Development Environment

---

# KPI Examples

## Workforce KPIs
- Total employees
- Employees per department
- Employees per region
- Employees per role

## Compensation KPIs
- Average salary
- Salary distribution
- Top paying departments
- Min/Max salary

## Hiring KPIs
- Hiring trends by year
- Growth rate analysis

---

# Dashboard

The dashboard was built using:
- Streamlit
- DuckDB
- exported Gold parquet datasets

It includes:
- KPI cards
- hiring trend charts
- department analysis
- compensation analytics
- workforce visualizations

---

# Project Structure

```text
hr-lakehouse-project/
├── dashboard/
│   ├── app.py
│   ├── requirements.txt
│   ├── data/
│
├── extract/
├── notebooks/
├── spark/
│   ├── docker-compose.yml
│   ├── requirements.txt
│
├── README.md
├── .gitignore
```

---



# Future Improvements

- CDC implementation
- Structured Streaming
- Airflow orchestration
- Incremental pipelines
- Delta optimization
- dbt integration
- Data quality checks
- CI/CD deployment
- Kubernetes deployment
