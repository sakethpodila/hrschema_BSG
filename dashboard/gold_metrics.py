import streamlit as st
import pandas as pd
import duckdb
from pathlib import Path

# ---------------------------------
# Page Config
# ---------------------------------

st.set_page_config(
    page_title='dashboard',
    layout='wide'
)

# ---------------------------------
# Title
# ---------------------------------

st.title('HR Schema Dashboard')

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
# ---------------------------------
# DuckDB Connection
# ---------------------------------

con = duckdb.connect()

# ---------------------------------
# Load Parquet Files
# ---------------------------------

workforce_df = con.execute(f"""
SELECT *
FROM read_parquet(
    '{DATA_DIR / "workforce_summary_kpis.parquet"}'
)
""").df()

compensation_df = con.execute(f"""
SELECT *
FROM read_parquet(
    '{DATA_DIR / "compensation_summary_kpis.parquet"}'
)
""").df()

hiring_df = con.execute(f"""
SELECT *
FROM read_parquet(
    '{DATA_DIR / "hiring_trend_kpis.parquet"}'
)
""").df()

# ---------------------------------
# KPI Metrics
# ---------------------------------

total_employees = int(
    workforce_df['total_employees'].sum()
)

avg_salary = round(
    workforce_df['avg_salary'].mean(),
    2
)

total_departments = workforce_df[
    'department_name'
].nunique()

max_salary = round(
    compensation_df['max_salary'].max(),
    2
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    'Total Employees',
    total_employees
)

col2.metric(
    'Average Salary',
    avg_salary
)

col3.metric(
    'Departments',
    total_departments
)

col4.metric(
    'Highest Salary',
    max_salary
)

# ---------------------------------
# Workforce Summary
# ---------------------------------

st.subheader('Workforce Summary')

st.dataframe(
    workforce_df,
    use_container_width=True
)

# ---------------------------------
# Compensation Summary
# ---------------------------------

st.subheader('Compensation Summary')

st.dataframe(
    compensation_df,
    use_container_width=True
)

# ---------------------------------
# Hiring Trends
# ---------------------------------

st.subheader('Hiring Trends')

hiring_chart = hiring_df[
    ['hire_year', 'total_hires']
].set_index('hire_year')

st.line_chart(hiring_chart)

# ---------------------------------
# Employees per Department
# ---------------------------------

st.subheader('Employees per Department')

dept_chart = workforce_df[
    ['department_name', 'total_employees']
].set_index('department_name')

st.bar_chart(dept_chart)

# ---------------------------------
# Regional Workforce Distribution
# ---------------------------------

st.subheader('Regional Workforce Distribution')

region_chart = workforce_df.groupby(
    'region_name'
)['total_employees'].sum()

st.bar_chart(region_chart)

# ---------------------------------
# Top Paying Departments
# ---------------------------------

st.subheader('Top Paying Departments')

top_departments = workforce_df.sort_values(
    by='avg_salary',
    ascending=False
)

st.dataframe(
    top_departments[
        [
            'department_name',
            'avg_salary',
            'max_salary'
        ]
    ],
    use_container_width=True
)

# ---------------------------------
# Architecture Overview
# ---------------------------------

