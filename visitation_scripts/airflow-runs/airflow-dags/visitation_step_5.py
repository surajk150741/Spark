from __future__ import annotations
from datetime import datetime, timedelta
from airflow import DAG
# Operators; we need this to operate!
from airflow.providers.cncf.kubernetes.operators.spark_kubernetes import SparkKubernetesOperator
from airflow.providers.cncf.kubernetes.sensors.spark_kubernetes import SparkKubernetesSensor
from airflow.operators.empty import EmptyOperator


with DAG(
    dag_id="visitation_step_5",
    default_args={'max_active_runs': 1},
    description='submit visitation_step_5 as sparkApplication on kubernetes',
    schedule=timedelta(days=1),
    start_date=datetime(2021, 1, 1),
    catchup=False,
) as dag:
    t0 = EmptyOperator(task_id='airflow_health_check', retries=1, dag=dag)
    t1 = SparkKubernetesOperator(
        task_id='visitation_step_5',
        kubernetes_conn_id='kubernetes_default',
        namespace="airflow",
        application_file="templates/dm_pyspark_step_05.yaml",
        params={'input_date':  "{{ dag_run.conf['input_date'] }}", 'country': "{{ dag_run.conf['country'] }}"},
        do_xcom_push=True,
        dag=dag
    )
    t2 = SparkKubernetesSensor(
        
        task_id='visitation_step_5_monitor',
        kubernetes_conn_id='kubernetes_default',
        namespace="airflow",
        application_name="{{ task_instance.xcom_pull(task_ids='visitation_step_5')['metadata']['name'] }}",
        dag=dag,
    )
    t0 >> t1 >> t2