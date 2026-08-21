FROM apache/airflow:2.10.5-python3.12

USER airflow

RUN pip install --no-cache-dir pandas psycopg2-binary

COPY src /app/src
COPY airflow/dags /opt/airflow/dags

ENV PYTHONPATH=/app
