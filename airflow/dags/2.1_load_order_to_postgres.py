import datetime
import pendulum
import os

# import requests
from airflow import DAG
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.python import PythonOperator

with DAG(
    "2.1_load_order_detail_to_postgres",
    # These args will get passed on to each operator
    # You can override them on a per-task basis during operator initialization
    default_args={"retries": 2},
    description="DAG tutorial",
    schedule=None,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    tags=["datasource"],
) as dag:
    drop_order_detail_table = PostgresOperator(
        task_id="drop_order_detail_table",
        postgres_conn_id="metadata_db",
        sql="""DROP TABLE IF EXISTS order_detail;""",
    )

    create_order_detail_table = PostgresOperator(
        task_id="create_order_detail_table",
        postgres_conn_id="metadata_db",
        sql="""
            CREATE TABLE IF NOT EXISTS order_detail (
                "order_created_timestamp" TIMESTAMP,
                "status" TEXT,
                "price" INTEGER,
                "discount" FLOAT,
                "id" TEXT PRIMARY KEY NOT NULL,
                "drive_id" TEXT,
                "user_id" TEXT,
                "restaurant_id" TEXT
            );""",
    )

    def get_data():
        data_path = "/opt/airflow/sample/order_detail.csv"
        postgres_hook = PostgresHook(postgres_conn_id="metadata_db")
        conn = postgres_hook.get_conn()
        cur = conn.cursor()
        with open(data_path, "r") as file:
            cur.copy_expert(
                "COPY order_detail FROM STDIN WITH CSV HEADER DELIMITER AS ',' QUOTE '\"'",
                file,
            )
        conn.commit()

    load_data = PythonOperator(
        task_id="load_data_order_detail",
        python_callable=get_data,
    )

    # 395361
    query_order_detail = PostgresOperator(
        task_id="query_order_detail",
        postgres_conn_id="metadata_db",
        sql="""
        select count(*) from order_detail
        """,
    )

    drop_order_detail_table >> create_order_detail_table >> load_data >> query_order_detail
