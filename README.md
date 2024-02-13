
# Retail Invoices

Building a data pipeline using some modern data tech stack like DBT, GCP Big Query and the most famous orchestrator Apache Airflow. Also, using SODA to do the data quality check.

##Pre requesites
- Docker;
- Astro CLI (https://docs.astronomer.io/astro/cli/install-cli);
- Soda Data Quality Tool;
- Google Cloud Account.




## Tech Stack

**Orchestrator** Apache Airflow;

**Data Warehouse:** Big Query;

**Cloud:** Google Cloud Plataform;

**Data Transformation Tool:** DBT;

**DataQuality Tool":** Soda;


## Dataset
source: https://www.kaggle.com/datasets/tunguz/online-retail

Schema:
| Column      | Description                                                                                                                |
|-------------|----------------------------------------------------------------------------------------------------------------------------|
| InvoiceNo   | Invoice number. Nominal, a 6-digit integral number uniquely assigned to each transaction. If this code starts with the letter 'c', it indicates a cancellation. |
| StockCode   | Product (item) code. Nominal, a 5-digit integral number uniquely assigned to each distinct product.                        |
| Description | Product (item) name. Nominal.                                                                                              |
| Quantity    | The quantities of each product (item) per transaction. Numeric.                                                            |
| InvoiceDate | Invoice Date and time. Numeric, the day and time when each transaction was generated.                                       |
| UnitPrice   | Unit price. Numeric, Product price per unit in sterling.                                                                   |
| CustomerID  | Customer number. Nominal, a 5-digit integral number uniquely assigned to each customer.                                   |
| Country     | Country name. Nominal, the name of the country where each customer resides.                                                 |


DER:
![DER](https://github.com/matheusbudin/airflow-bq-dbt-soda/blob/main/images/data%20modeling.png)

## Pipeline Architecture
The following iamge shows the architecture used in this project.
**1.** The first thing that we need to do is secure the encoding from the csv file. Since Big Query could throw an error if its not on the UTF-8 encoding, this code will be shown in the following sections;

**2.** Ingest the raw data using apache airflow and its connector with google cloud storage;

**3.** Perform a quality check for the ingested data, such as verifying the column names and datatypes;

**4.** Build and deploy DBT models that do the transformation for the data so we can have the fact and dimention tables;

**5.** Once again perform a quality check;

**6.** Use DBT once more to build report tables, that will be used in Power Bi. Those and like simple querys from the fact and dimention tables, just to simplify our work when building the dashboard;

**7.** Perform one last quality check;

**8.** Build a dashboard report in power Bi.

Pipeline Archtecture:

![Pipeline](https://github.com/matheusbudin/airflow-bq-dbt-soda/blob/main/images/architecture.jpg)

## Step by Step - Tutorial
- Download the dataset from the website: https://www.kaggle.com/datasets/tunguz/online-retail;

- Extract and store the CSV file ```include/dataset/online_retail.csv```;

- Add in the ```requeriments.txt``` the folowing: ``` apache-airflow-providers-google==10.3.0```;

- Create a GCS bucket with an unique name: ``` <your-bucket-name>_online_retail```

- Go to IAM on GCP  -> create Service account -> ```your-service-account_name```

- Grant access to GCS + Big query  and create a Key by clicking on: service account -> Add key -> generate the json file;

- Copy this json file into your local astro project enviroment: ```include/gcp/service_account.json```
 - **IMPORTANT** do not forget to add its path inside .gitignore, by doing this your credentials will not bbe published and you will be secure.

- For instance your service_account.json may look like the following (and deleted by now) json:

```
# include/gcp/service_account.json

{
    "type": "service_account",
    "project_id": "airtube-390719",
    "private_key_id": "58cfee8a937e7bfc66ae6465a848db53cf4fb919",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCs1DzaHpGl7zcw\nD/Ab2VDs1YxKK7rnT8Oi+pJwxomLGEg15q2mgbS8tebrs65lC8Ihzs3SGfaBycWK\nlMqOLP95gTnsYgMpveoCv/L9OU8UiYTbPdJEk7YxJi0u7jYl0BD2WJ5NnpUdBFYH\nEzAs9X5/3sHRqQItLtxMVEQ5kG4Q0kPeGFGMhABksuBkZ8EtwdVxsNQFUk9GAdJb\nWLa6Co3DraFd3A3QXCfO8HHmdR4YxqX6MKOpAipDied6PYUhf+uZoW9FFXg4VLSz\n0INYkmIhxmv+3jNcHS0wCUFS/GunRzvk9gh61HpF6KvM4OBuRSKLWt1Jezsww4hl\nQbJYOnbTAgMBAAECggEAJ6IgNlDuS6Q4/q+Y+3nxge5S1quCmAsFrTlTHcOZxSkT\nXjEBP37dKK16QDEbXBa/NSuMrZLAofDYeTg33zTYfU+yLdAoM4lWwbytB3798JK8\nwd5CevF4xXqgv/NmvXMigKu/2cL1JQtagxLWaGj/0mkN/3uHgT8Oy/5DCwRhCUAe\nIFtpzCLp4fFrkpRcXXcKKL7zsxt9x4ya0qiYA/q1p7y4zl3734ZxGw48MPVeLGSE\ne46cVMBBlDYgdsnwLJA7IexbIrg5viw4m7HG9QMUaoU1vb7xgQSEX0VM+4z3mznH\nYEJ6CAYlEDmcqAegTNayyMRFWej6ZdbgN7h+ju0uoQKBgQDf9Q8eIaM6TDlOJBrX\nBhv8eIraaGbP6EBFbc8m7jp8JwtuHrdcPzxH5euxwRWnpF8HzH7ea7+EXKvRhuTf\n5y5+biMquK5USGEp1pN/ehaOpXjgMvNZ9qRTVPWjgKM4hjER12xSuVEjqFP3yTG6\nqZyGqu/ylVC8glJp1Zdm1atvowKBgQDFjn4REXBVdDajED/ZydYPNllBi6CegNJs\nshDDlgIElyjKn7pqgrEK3F+sJSRWHJni9Z4mRjokgW/H4us9Bh6rzOEqJRZOs8WS\ndnNBp24W8iprBj8K7l8xCbzTRqwz0wgM0oS/irILGUSyn6ye9I65WqaZ28xCTMhm\nNkKSYVSPEQKBgQDc25j7CAUmmsDwlJ57aqTyyBV26fpqEgo/7diZ9dlrUj3tbRE6\nQYo7BTz4YQfv+SNWV47N3chSyekPik3vmNa7C/ZWTSZuK6rWTavLzSStq/WWc+iU\n0aygGWrcwSE1vvBpPd6vfd3MolWcSKdoA5g/HhffTOz/2i1X/bF/UjvsrQKBgQCr\nr9EZjjk82pldDxMed40jfU0GbIzzEutMcVemUmiAisl1hmjghaHM2YX/ueuhNov6\nNRDzHFcNQLvfT/K1/uqKzavlD4Qac5tBVNWHejVvlZeNmUkSe+SYXmkOh73B8CVv\n10hsmeFvSc9tGN1Q6yJaLVDaJ62U9Nu4EHG8ev+csQKBgCI8ivxrXdn0NwTThb2j\nHfw0CNAHNl1c2ml7lhmSE+pF5uIxlVHwETP7gz2+hSd85AqxG6+mkHZhu4kzwcGh\niI0iIMYARP9Al9SC1dgMjQz28VEctBRs3aiDUPKBkFESig7ZHhy6cxGUkZZdUpKZ\n6jaiEqIIqBLNAATTx+AO/b+R\n-----END PRIVATE KEY-----\n",
    "client_email": "airflow-online-retail@airtube-390719.iam.gserviceaccount.com",
    "client_id": "117189738213106346790",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/airflow-online-retail%40airtube-390719.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
}service_accountservice_account
```
# airflow configuration

- Go to local:8080, this should open your airflow webpage (once you have deployed it: "bash terminal: ```astro dev start```);
- Go to the tab "Admin", then click in "Conections" and type: **id:** gcp / **type:** Google Cloud / **Keypath Path:** ```/usr/local/airflow/include/gcp/service_account.json```
- Test the connection.

#Creating the Dag:

- On the dag folder, create a file ```reatil.py```

```
# retail.py

from airflow.decorators import dag, task
from datetime import datetime

from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator

@dag(
    start_date=datetime(4, 1, 1),
    schedule=None,
    catchup=False,
    tags=['retail'],
)
def retail():

    upload_csv_to_gcs = LocalFilesystemToGCSOperator(
        task_id='upload_csv_to_gcs',
        src='include/dataset/online_retail.csv',
        dst='raw/online_retail.csv',
        bucket='marclamberti_online_retail',
        gcp_conn_id='gcp',
        mime_type='text/csv',
    )

retail()
```

- Test you dag by entering the container with the first command and testing with the second command as follows:

```
astro dev bash
airflow tasks test retail upload_csv_to_gcs 2024-01-01
```

#Creating an empty Dataset on bigquery (which is equivalent to a Schema on a Database):

```
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateEmptyDatasetOperator

create_retail_dataset = BigQueryCreateEmptyDatasetOperator(
        task_id='create_retail_dataset',
        dataset_id='retail',
        gcp_conn_id='gcp',
    )
```
# Create a task to load the data into bigquery inside the dataset, and call it raw_invoices table:

```
from astro import sql as aql
from astro.files import File
from astro.sql.table import Table, Metadata
from astro.constants import FileType

gcs_to_raw = aql.load_file(
        task_id='gcs_to_raw',
        input_file=File(
            'gs://marclamberti_online_retail/raw/online_retail.csv',
            conn_id='gcp',
            filetype=FileType.CSV,
        ),
        output_table=Table(
            name='raw_invoices',
            conn_id='gcp',
            metadata=Metadata(schema='retail')
        ),
        use_native_support=False,
    )
```

## By now we already have our raw data succesfully loaded into big query as ```raw_invoice``` table

## Installing SODA, a data quality tool:

- Input ```soda-core-bigquery==3.0.45``` in the requeriments.txt

- Create a folder called "soda" inside "include" path, and create  ```configuration.yml```:

```
-- include/soda/configuration.yml
data_source retail:
  type: bigquery
  connection:
    account_info_json_path: /usr/local/airflow/include/gcp/service_account.json
    auth_scopes:
    - https://www.googleapis.com/auth/bigquery
    - https://www.googleapis.com/auth/cloud-platform
    - https://www.googleapis.com/auth/drive
    project_id: '<YOUR_GCP_PROJECT_ID>'
    dataset: retail
```
- Assuming you already have an account on SODA, create a API key, so that airflow can connect: By clicking on Profile -> API Keys -> Create API -> Copy the code generated into ```configuration.yml```
it should look like this:
```
data_source retail:
  type: bigquery
  connection:
    account_info_json_path: /usr/local/airflow/include/gcp/service_account.json
    auth_scopes:
    - https://www.googleapis.com/auth/bigquery
    - https://www.googleapis.com/auth/cloud-platform
    - https://www.googleapis.com/auth/drive
    project_id: '<YOUR_GCP_PROJECT_ID>'
    dataset: retail
soda_cloud:
  host: cloud.us.soda.io
  api_key_id: <YOUR_ID>
  api_key_secret: <YOUR API SECRET>
```
- Test the connection by typing:

```
astro dev bash
soda test-connection -d retail -c include/soda/configuration.yml
```
- Create ```raw_invoices.yml``` as a first data quality test as follows:
```
#include/soda/checks/sources/raw_invoices.yml

checks for raw_invoices:
  - schema:
      fail:
        when required column missing: [InvoiceNo, StockCode, Quantity, InvoiceDate, UnitPrice, CustomerID, Country]
        when wrong column type:
          InvoiceNo: string
          StockCode: string
          Quantity: integer
          InvoiceDate: string
          UnitPrice: float64
          CustomerID: float64
          Country: string
```
This quality checks the columns data type, and if the columns listed exist.

- run the quality check test:
```soda scan -d retail -c include/soda/configuration.yml include/soda/checks/sources/raw_invoices.yml```

- Create your check function:
For this we will be creating a external python that will be installed by adding in the docker file:
```
# install soda into a virtual environment
RUN python -m venv soda_venv && source soda_venv/bin/activate && \
    pip install --no-cache-dir soda-core-bigquery==3.0.45 &&\
    pip install --no-cache-dir soda-core-scientific==3.0.45 && deactivate
```
**This will help the data checks test to run inside the dag without creating conflict with the internal airflow python that is executing the tasks.**

- Create the function code (the path its in the first line commented):
```
# include/soda/check_function.py
def check(scan_name, checks_subpath=None, data_source='retail', project_root='include'):
    from soda.scan import Scan

    print('Running Soda Scan ...')
    config_file = f'{project_root}/soda/configuration.yml'
    checks_path = f'{project_root}/soda/checks'

    if checks_subpath:
        checks_path += f'/{checks_subpath}'

    scan = Scan()
    scan.set_verbose()
    scan.add_configuration_yaml_file(config_file)
    scan.set_data_source_name(data_source)
    scan.add_sodacl_yaml_files(checks_path)
    scan.set_scan_definition_name(scan_name)

    result = scan.execute()
    print(scan.get_logs_text())

    if result != 0:
        raise ValueError('Soda Scan failed')

    return result

```
- In the dag code add:
```
@task.external_python(python='/usr/local/airflow/soda_venv/bin/python')
    def check_load(scan_name='check_load', checks_subpath='sources'):
        from include.soda.check_function import check

        return check(scan_name, checks_subpath)

```
**ExternalPython uses an existing python virtual environment with dependencies pre-installed. That makes it faster to run than the VirtualPython where dependencies are installed at each run**

- Test your task:
```
astro dev bash
airflow tasks test retail check_load 2024-01-01
```
With this we have completed the Soda setting up and configured to run the data quality checks.
