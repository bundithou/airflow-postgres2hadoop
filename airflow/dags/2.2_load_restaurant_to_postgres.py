import datetime
import pendulum
import os

# import requests
from airflow import DAG
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.python import PythonOperator

with DAG(
    "2.1_load_restaurant_detail_to_postgres",
    # These args will get passed on to each operator
    # You can override them on a per-task basis during operator initialization
    default_args={"retries": 2},
    description="DAG tutorial",
    schedule=None,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    tags=["datasource"],
) as dag:
    drop_restaurant_detail_table = PostgresOperator(
        task_id="drop_restaurant_detail_table",
        postgres_conn_id="metadata_db",
        sql="""DROP TABLE IF EXISTS restaurant_detail;""",
    )

    create_restaurant_detail_table = PostgresOperator(
        task_id="create_restaurant_detail_table",
        postgres_conn_id="metadata_db",
        sql="""
            CREATE TABLE IF NOT EXISTS restaurant_detail (
                id TEXT PRIMARY KEY NOT NULL,
                restaurant_name TEXT,
                category TEXT,
                estimated_cooking_time FLOAT,
                latitude FLOAT,
                longitude FLOAT
            );""",
    )

    def get_data():
        data_path = "/opt/airflow/sample/restaurant_detail.csv"
        postgres_hook = PostgresHook(postgres_conn_id="metadata_db")
        conn = postgres_hook.get_conn()
        cur = conn.cursor()
        with open(data_path, "r") as file:
            cur.copy_expert(
                "COPY restaurant_detail FROM STDIN WITH CSV HEADER DELIMITER AS ',' QUOTE '\"'",
                file,
            )
        conn.commit()

    load_data = PythonOperator(
        task_id="load_data_restaurant_detail",
        python_callable=get_data,
    )

    # 395361
    query_restaurant_detail = PostgresOperator(
        task_id="query_restaurant_detail",
        postgres_conn_id="metadata_db",
        sql="""
        select count(*) from restaurant_detail
        """,
    )

    drop_restaurant_detail_table >> create_restaurant_detail_table >> load_data >> query_restaurant_detail
