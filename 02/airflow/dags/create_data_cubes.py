from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import population
import care_providers
import urllib
import os

def download_file(url, output_file):
    urllib.request.urlretrieve(url, output_file)

def create_folders(output_path):
    if not os.path.exists("./data"):
        os.mkdir("./data")

    if not os.path.exists(output_path):
        os.mkdir(output_path)


dag_args = {
    "email": ["codprojmail@gmail.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    'retry_delay': timedelta(minutes=15),
    "output_path": "./output/",
}

with DAG(
    dag_id="data-cubes",
    default_args=dag_args,
    start_date=datetime(2023, 3, 26),
    schedule=None,
    catchup=False,
    tags=["NDBI046"],
) as dag:
    create_folders_task = PythonOperator(
        task_id='create_folders',
        python_callable=create_folders,
        op_kwargs={
            'output_path': dag_args['output_path']
        },
        dag=dag
    )
    
    download_population_task = PythonOperator(
        task_id='download_population',
        python_callable=download_file,
        op_kwargs={
            'url': 'https://www.czso.cz/documents/10180/184344914/130141-22data2021.csv',
            'output_file': 'data/pohyb-obyvatel.csv'
        },
        dag=dag
    )
    
    download_care_providers_task = PythonOperator(
        task_id='download_care_providers',
        python_callable=download_file,
        op_kwargs={
            'url': 'https://raw.githubusercontent.com/bmazou/Data-engineering-hw/main/01/data/care_providers.csv',
            'output_file': 'data/care_providers.csv'
        },
        dag=dag
    )
    
    download_nuts_task = PythonOperator(
        task_id='download_nuts',
        python_callable=download_file,
        op_kwargs={
            'url': 'https://raw.githubusercontent.com/bmazou/Data-engineering-hw/main/01/data/ciselnik-okresu.csv',
            'output_file': 'data/ciselnik-okresu.csv'
        },
        dag=dag
    )

    run_population_task = PythonOperator(
        task_id='run_population',
        python_callable=population.main,
        op_kwargs={
            'output_dir': dag_args['output_path']
        },
        dag=dag
    )
    
    run_care_providers_task = PythonOperator(
        task_id='run_care_providers',
        python_callable=care_providers.main,
        op_kwargs={
            'output_dir': dag_args['output_path']
        },
        dag=dag
    )

    create_folders_task >> [download_nuts_task, download_population_task] >> run_population_task
    create_folders_task >> download_care_providers_task >> run_care_providers_task
