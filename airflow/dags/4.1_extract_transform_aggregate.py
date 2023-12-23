"""
Example Airflow DAG to submit Apache Spark applications using
`SparkSubmitOperator`, `SparkJDBCOperator` and `SparkSqlOperator`.
"""
from __future__ import annotations

import os
from datetime import datetime

from airflow.models import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator

with DAG(
    dag_id="4_extract_transform_aggregate",
    schedule=None,
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=["extract", "transform", "aggregate"],
) as dag:
    start = EmptyOperator(task_id="start")
    end = EmptyOperator(task_id="end")
    # check dependency

    # start extract transform
    end_et = EmptyOperator(task_id="end_et")
    tables = ["order_detail", "restaurant_detail"]
    for table in tables:
        # extract data from postgres
        extract = SparkSubmitOperator(
            task_id=f"extract_{table}",
            application=f"/usr/local/spark/src/extract_{table}.py",
            driver_class_path="/usr/local/spark/jars/postgresql-42.7.0.jar"
        )

        # transform data into parquet
        transform = SparkSubmitOperator(
            task_id=f"transform_{table}",
            application=f"/usr/local/spark/src/transform_{table}.py"
        )

        start >> extract >> transform >> end_et

    # end extract transform
        
    # start aggregate
    aggregate = SparkSubmitOperator(
        task_id=f"aggregate",
        application=f"/usr/local/spark/src/aggregate.py"
    )
    end_et >> aggregate >> end
    # end aggregate