import streamlit as st
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

st.set_page_config(
    page_title="HR Lakehouse Analytics",
    layout="wide"
)

st.title("HR Workforce Analytics Lakehouse")

# -------------------------
# Spark Session
# -------------------------

spark = SparkSession.builder \
    .appName("StreamlitLakehouse") \
    .config(
        "spark.jars.packages",
        ",".join([
            "io.delta:delta-spark_2.12:3.0.0",
            "org.apache.hadoop:hadoop-aws:3.3.4",
            "com.amazonaws:aws-java-sdk-bundle:1.12.262"
        ])
    ) \
    .config(
        "spark.sql.extensions",
        "io.delta.sql.DeltaSparkSessionExtension"
    ) \
    .config(
        "spark.sql.catalog.spark_catalog",
        "org.apache.spark.sql.delta.catalog.DeltaCatalog"
    ) \
    .config(
        "spark.hadoop.fs.s3a.endpoint",
        "http://host.docker.internal:9000"
    ) \
    .config(
        "spark.hadoop.fs.s3a.access.key",
        "minioadmin"
    ) \
    .config(
        "spark.hadoop.fs.s3a.secret.key",
        "minioadmin"
    ) \
    .config(
        "spark.hadoop.fs.s3a.path.style.access",
        "true"
    ) \
    .config(
        "spark.hadoop.fs.s3a.impl",
        "org.apache.hadoop.fs.s3a.S3AFileSystem"
    ) \
    .getOrCreate()

# -------------------------
# Load Gold Tables
# -------------------------

workforce_df = spark.read.format("delta").load(
    "s3a://lakehouse/gold/workforce_kpis"
)

compensation_df = spark.read.format("delta").load(
    "s3a://lakehouse/gold/compensation_kpis"
)

# -------------------------
# KPI Section
# -------------------------

employees_silver_df = spark.read.format("delta").load(
    "s3a://lakehouse/silver/employees_enriched"
)

total_employees = employees_silver_df.count()

avg_salary = employees_silver_df.agg(
    F.avg("SALARY")
).collect()[0][0]

total_departments = employees_silver_df.select(
    "DEPARTMENT_NAME"
).distinct().count()

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Employees",
    total_employees
)

col2.metric(
    "Average Salary",
    round(avg_salary, 2)
)

col3.metric(
    "Departments",
    total_departments
)

# -------------------------
# Workforce Summary
# -------------------------

st.subheader("Workforce KPIs")

st.dataframe(
    workforce_df.toPandas()
)

# -------------------------
# Compensation Summary
# -------------------------

st.subheader("Compensation KPIs")

st.dataframe(
    compensation_df.toPandas()
)

# -------------------------
# Workforce Chart
# -------------------------

st.subheader("Employees per Department")

dept_chart = employees_silver_df.groupBy(
    "DEPARTMENT_NAME"
).agg(
    F.count("*").alias("EMPLOYEE_COUNT")
).toPandas()

st.bar_chart(
    dept_chart.set_index("DEPARTMENT_NAME")
)