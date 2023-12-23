"""
Example Airflow DAG to submit Apache Spark applications using
`SparkSubmitOperator`, `SparkJDBCOperator` and `SparkSqlOperator`.
"""
from __future__ import annotations

import os
from datetime import datetime

from airflow.models import DAG
# from airflow.providers.apache.spark.operators.spark_jdbc import SparkJDBCOperator
# from airflow.providers.apache.spark.operators.spark_sql import SparkSqlOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="3.2_extract_restaurant_detail_to_parquet",
    schedule=None,
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=["extract", "ingestion"],
) as dag:
    # check dependency

    # extract job
    submit_sparkjob = SparkSubmitOperator(
        task_id="submit_sparkjob",
        application="/usr/local/spark/src/extract_restaurant_detail.py",
        driver_class_path="/usr/local/spark/jars/postgresql-42.7.0.jar",
    )

    submit_sparkjob 
    # >> submit_bashjob