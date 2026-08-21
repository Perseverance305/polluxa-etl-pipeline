from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from src.main import main

PIPELINE_NAME = 'linkedin_leads_pipeline'

def run_pipeline():
    main()

default_args = {
    'owner': 'polluxa',
    'depends_on_past': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id=PIPELINE_NAME,
    description='Orchestrates the LinkedIn leads ETL pipeline',
    default_args=default_args,
    start_date=datetime(2026, 8, 1),
    schedule='0 6 * * *',
    catchup=False,
    max_active_runs=1,
    tags=['polluxa', 'etl', 'linkedin', 'data-quality'],
 ) as dag:

    run_etl_pipeline = PythonOperator(
        task_id='run_etl_pipeline',
        python_callable=run_pipeline,
    )

run_etl_pipeline
