from airflow.decorators import dag, task
from datetime import datetime
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateEmptyDatasetOperator
from astro import sql as aql
from astro.files import File
from astro.sql.table import Table, Metadata
from astro.constants import FileType
from airflow.operators.python import PythonOperator
import chardet
import os

@dag(
  start_date=datetime(2024, 1, 1),
  schedule=None,
  catchup=False,
  tags=['retail'],
)
def retail_utf8():
    input_csv_path = '/usr/local/airflow/include/dataset/online_retail.csv'
    output_csv_path = '/usr/local/airflow/include/dataset/online_retail_utf8.csv'

    def detect_encoding():
        with open(input_csv_path, 'rb') as file:
            result = chardet.detect(file.read())
        return result['encoding']

    def convert_to_utf8():
        print(f"Converting {input_csv_path} to UTF-8")

        encoding = detect_encoding()

        with open(input_csv_path, 'r', encoding=encoding) as file:
            data = file.read()

        with open(output_csv_path, 'w', encoding='utf-8', newline='') as file:
            file.write(data)

        print(f"Conversion complete. Output file: {output_csv_path}")

    upload_csv_to_gcs = LocalFilesystemToGCSOperator(
        task_id='upload_csv_to_gcs',
        src=input_csv_path,
        dst='raw/online_retail_utf8.csv',
        bucket='matheusrbudin-airflow-retail-project',
        gcp_conn_id='gcp',
        mime_type='text/csv'
    )

    create_retail_dataset = BigQueryCreateEmptyDatasetOperator(
        task_id='create_retail_dataset',
        dataset_id='retail_fixed_encoding',
        gcp_conn_id='gcp',
    )

    detect_and_convert_encoding = PythonOperator(
        task_id='detect_and_convert_encoding',
        python_callable=convert_to_utf8
    )

    gcs_to_raw = aql.load_file(
        task_id='gcs_to_raw',
        input_file=File(
            'gs://matheusrbudin-airflow-retail-project/raw/online_retail_utf8.csv',
            conn_id='gcp',
            filetype=FileType.CSV,
        ),
        output_table=Table(
            name='raw_invoices_fixed_encoding',
            conn_id='gcp',
            metadata=Metadata(schema='retail')
        ),
        use_native_support=False,
    )

    # Set task dependencies
    detect_and_convert_encoding >> upload_csv_to_gcs >> create_retail_dataset  >> gcs_to_raw

retail_utf8()
