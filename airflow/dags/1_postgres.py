import datetime
import pendulum
import os

import requests
# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.postgres.operators.postgres import PostgresOperator

with DAG(
    "1_test_postgres",
    # These args will get passed on to each operator
    # You can override them on a per-task basis during operator initialization
    default_args={"retries": 2},
    description="DAG tutorial",
    schedule=None,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    tags=["example"],
) as dag:
    create_employees_temp_table = PostgresOperator(
        task_id="test_postgres",
        postgres_conn_id="metadata_db",
        sql="""
        select * from information_schema.tables
        """,
    )

    create_employees_temp_table