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
    dag_id="4_extract_transform_aggregate_seq",
    schedule=None,
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=["extract", "transform", "aggregate"],
) as dag:
    start = EmptyOperator(task_id="start")
    end = EmptyOperator(task_id="end")
    # check dependency

    # start extract transform
    tables = ["order_detail", "restaurant_detail"]
    # extract data from postgres
    table = tables[0]
    extract_o = SparkSubmitOperator(
        task_id=f"extract_{table}",
        application=f"/usr/local/spark/src/extract_{table}.py",
        driver_class_path="/usr/local/spark/jars/postgresql-42.7.0.jar"
    )

    # transform data into parquet
    transform_o = SparkSubmitOperator(
        task_id=f"transform_{table}",
        application=f"/usr/local/spark/src/transform_{table}.py"
    )
    end_et_o = EmptyOperator(task_id=f"end_et_{table}")

    # extract data from postgres
    table = tables[1]
    extract_r = SparkSubmitOperator(
        task_id=f"extract_{table}",
        application=f"/usr/local/spark/src/extract_{table}.py",
        driver_class_path="/usr/local/spark/jars/postgresql-42.7.0.jar"
    )

    # transform data into parquet
    transform_r = SparkSubmitOperator(
        task_id=f"transform_{table}",
        application=f"/usr/local/spark/src/transform_{table}.py"
    )
    end_et_r = EmptyOperator(task_id=f"end_et_{table}")

    

    # end extract transform
        
    # start aggregate
    aggregate = SparkSubmitOperator(
        task_id=f"aggregate",
        application=f"/usr/local/spark/src/aggregate.py"
    )
    # end aggregate
    start >> extract_o >> transform_o >> end_et_o >> extract_r >> transform_r >> end_et_r >> aggregate >> end
