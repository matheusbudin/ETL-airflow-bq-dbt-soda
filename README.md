
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

#Transform (DBT)

- in the requirements.txt type:
```
// both of this are already being installed with the last two dependencies
// REMOVE apache-airflow-providers-google==10.3.0
// REMOVE soda-core-bigquery==3.0.45
astronomer-cosmos[dbt-bigquery]>=1.0.3 // install google + cosmos + dbt
protobuf==3.20.0
```
- add env variable:
```PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python```

- In the Docker File type:
```
# install dbt into a virtual environment
RUN python -m venv dbt_venv && source dbt_venv/bin/activate && \
    pip install --no-cache-dir dbt-bigquery==1.5.3 && deactivate
```
- restart your project by typing in the terminal:
```astro dev restart```

# Create a ```include/dbt``` folder:
- create a file called: ```packages.yml```:
```
# packages.yml
packages:
  - package: dbt-labs/dbt_utils
    version: 1.1.1
```
- create a dbt_project.yml file:
```
# dbt_project.yml

name: 'retail'

profile: 'retail'

models:
  retail:
    materialized: table
```
- create a profiles.yml file:
```# profiles.yml

retail:
 target: dev
 outputs:
  dev:
    type: bigquery
    method: service-account
    keyfile: /usr/local/airflow/include/gcp/service_account.json
    project: airtube-390719
    dataset: retail
    threads: 1
    timeout_seconds: 300
    location: US
```

# Now go to bigquery and create the following table, by executing the SQL command in its query IDE:
```
CREATE TABLE IF NOT EXISTS `retail.country` (
  `id` INT NOT NULL,
  `iso` STRING NOT NULL,
  `name` STRING NOT NULL,
  `nicename` STRING NOT NULL,
  `iso3` STRING DEFAULT NULL,
  `numcode` INT DEFAULT NULL,
  `phonecode` INT NOT NULL,
);

--
-- Dumping data for table `country`
--

INSERT INTO `retail.country` (`id`, `iso`, `name`, `nicename`, `iso3`, `numcode`, `phonecode`) VALUES
(1, 'AF', 'AFGHANISTAN', 'Afghanistan', 'AFG', 4, 93),
(2, 'AL', 'ALBANIA', 'Albania', 'ALB', 8, 355),
(3, 'DZ', 'ALGERIA', 'Algeria', 'DZA', 12, 213),
(4, 'AS', 'AMERICAN SAMOA', 'American Samoa', 'ASM', 16, 1684),
(5, 'AD', 'ANDORRA', 'Andorra', 'AND', 20, 376),
(6, 'AO', 'ANGOLA', 'Angola', 'AGO', 24, 244),
(7, 'AI', 'ANGUILLA', 'Anguilla', 'AIA', 660, 1264),
(8, 'AQ', 'ANTARCTICA', 'Antarctica', NULL, NULL, 0),
(9, 'AG', 'ANTIGUA AND BARBUDA', 'Antigua and Barbuda', 'ATG', 28, 1268),
(10, 'AR', 'ARGENTINA', 'Argentina', 'ARG', 32, 54),
(11, 'AM', 'ARMENIA', 'Armenia', 'ARM', 51, 374),
(12, 'AW', 'ARUBA', 'Aruba', 'ABW', 533, 297),
(13, 'AU', 'AUSTRALIA', 'Australia', 'AUS', 36, 61),
(14, 'AT', 'AUSTRIA', 'Austria', 'AUT', 40, 43),
(15, 'AZ', 'AZERBAIJAN', 'Azerbaijan', 'AZE', 31, 994),
(16, 'BS', 'BAHAMAS', 'Bahamas', 'BHS', 44, 1242),
(17, 'BH', 'BAHRAIN', 'Bahrain', 'BHR', 48, 973),
(18, 'BD', 'BANGLADESH', 'Bangladesh', 'BGD', 50, 880),
(19, 'BB', 'BARBADOS', 'Barbados', 'BRB', 52, 1246),
(20, 'BY', 'BELARUS', 'Belarus', 'BLR', 112, 375),
(21, 'BE', 'BELGIUM', 'Belgium', 'BEL', 56, 32),
(22, 'BZ', 'BELIZE', 'Belize', 'BLZ', 84, 501),
(23, 'BJ', 'BENIN', 'Benin', 'BEN', 204, 229),
(24, 'BM', 'BERMUDA', 'Bermuda', 'BMU', 60, 1441),
(25, 'BT', 'BHUTAN', 'Bhutan', 'BTN', 64, 975),
(26, 'BO', 'BOLIVIA', 'Bolivia', 'BOL', 68, 591),
(27, 'BA', 'BOSNIA AND HERZEGOVINA', 'Bosnia and Herzegovina', 'BIH', 70, 387),
(28, 'BW', 'BOTSWANA', 'Botswana', 'BWA', 72, 267),
(29, 'BV', 'BOUVET ISLAND', 'Bouvet Island', NULL, NULL, 0),
(30, 'BR', 'BRAZIL', 'Brazil', 'BRA', 76, 55),
(31, 'IO', 'BRITISH INDIAN OCEAN TERRITORY', 'British Indian Ocean Territory', NULL, NULL, 246),
(32, 'BN', 'BRUNEI DARUSSALAM', 'Brunei Darussalam', 'BRN', 96, 673),
(33, 'BG', 'BULGARIA', 'Bulgaria', 'BGR', 100, 359),
(34, 'BF', 'BURKINA FASO', 'Burkina Faso', 'BFA', 854, 226),
(35, 'BI', 'BURUNDI', 'Burundi', 'BDI', 108, 257),
(36, 'KH', 'CAMBODIA', 'Cambodia', 'KHM', 116, 855),
(37, 'CM', 'CAMEROON', 'Cameroon', 'CMR', 120, 237),
(38, 'CA', 'CANADA', 'Canada', 'CAN', 124, 1),
(39, 'CV', 'CAPE VERDE', 'Cape Verde', 'CPV', 132, 238),
(40, 'KY', 'CAYMAN ISLANDS', 'Cayman Islands', 'CYM', 136, 1345),
(41, 'CF', 'CENTRAL AFRICAN REPUBLIC', 'Central African Republic', 'CAF', 140, 236),
(42, 'TD', 'CHAD', 'Chad', 'TCD', 148, 235),
(43, 'CL', 'CHILE', 'Chile', 'CHL', 152, 56),
(44, 'CN', 'CHINA', 'China', 'CHN', 156, 86),
(45, 'CX', 'CHRISTMAS ISLAND', 'Christmas Island', NULL, NULL, 61),
(46, 'CC', 'COCOS (KEELING) ISLANDS', 'Cocos (Keeling) Islands', NULL, NULL, 672),
(47, 'CO', 'COLOMBIA', 'Colombia', 'COL', 170, 57),
(48, 'KM', 'COMOROS', 'Comoros', 'COM', 174, 269),
(49, 'CG', 'CONGO', 'Congo', 'COG', 178, 242),
(50, 'CD', 'CONGO, THE DEMOCRATIC REPUBLIC OF THE', 'Congo, the Democratic Republic of the', 'COD', 180, 242),
(51, 'CK', 'COOK ISLANDS', 'Cook Islands', 'COK', 184, 682),
(52, 'CR', 'COSTA RICA', 'Costa Rica', 'CRI', 188, 506),
(53, 'CI', "COTE D''IVOIRE", "Cote D''Ivoire", 'CIV', 384, 225),
(54, 'HR', 'CROATIA', 'Croatia', 'HRV', 191, 385),
(55, 'CU', 'CUBA', 'Cuba', 'CUB', 192, 53),
(56, 'CY', 'CYPRUS', 'Cyprus', 'CYP', 196, 357),
(57, 'CZ', 'CZECH REPUBLIC', 'Czech Republic', 'CZE', 203, 420),
(58, 'DK', 'DENMARK', 'Denmark', 'DNK', 208, 45),
(59, 'DJ', 'DJIBOUTI', 'Djibouti', 'DJI', 262, 253),
(60, 'DM', 'DOMINICA', 'Dominica', 'DMA', 212, 1767),
(61, 'DO', 'DOMINICAN REPUBLIC', 'Dominican Republic', 'DOM', 214, 1809),
(62, 'EC', 'ECUADOR', 'Ecuador', 'ECU', 218, 593),
(63, 'EG', 'EGYPT', 'Egypt', 'EGY', 818, 20),
(64, 'SV', 'EL SALVADOR', 'El Salvador', 'SLV', 222, 503),
(65, 'GQ', 'EQUATORIAL GUINEA', 'Equatorial Guinea', 'GNQ', 226, 240),
(66, 'ER', 'ERITREA', 'Eritrea', 'ERI', 232, 291),
(67, 'EE', 'ESTONIA', 'Estonia', 'EST', 233, 372),
(68, 'ET', 'ETHIOPIA', 'Ethiopia', 'ETH', 231, 251),
(69, 'FK', 'FALKLAND ISLANDS (MALVINAS)', 'Falkland Islands (Malvinas)', 'FLK', 238, 500),
(70, 'FO', 'FAROE ISLANDS', 'Faroe Islands', 'FRO', 234, 298),
(71, 'FJ', 'FIJI', 'Fiji', 'FJI', 242, 679),
(72, 'FI', 'FINLAND', 'Finland', 'FIN', 246, 358),
(73, 'FR', 'FRANCE', 'France', 'FRA', 250, 33),
(74, 'GF', 'FRENCH GUIANA', 'French Guiana', 'GUF', 254, 594),
(75, 'PF', 'FRENCH POLYNESIA', 'French Polynesia', 'PYF', 258, 689),
(76, 'TF', 'FRENCH SOUTHERN TERRITORIES', 'French Southern Territories', NULL, NULL, 0),
(77, 'GA', 'GABON', 'Gabon', 'GAB', 266, 241),
(78, 'GM', 'GAMBIA', 'Gambia', 'GMB', 270, 220),
(79, 'GE', 'GEORGIA', 'Georgia', 'GEO', 268, 995),
(80, 'DE', 'GERMANY', 'Germany', 'DEU', 276, 49),
(81, 'GH', 'GHANA', 'Ghana', 'GHA', 288, 233),
(82, 'GI', 'GIBRALTAR', 'Gibraltar', 'GIB', 292, 350),
(83, 'GR', 'GREECE', 'Greece', 'GRC', 300, 30),
(84, 'GL', 'GREENLAND', 'Greenland', 'GRL', 304, 299),
(85, 'GD', 'GRENADA', 'Grenada', 'GRD', 308, 1473),
(86, 'GP', 'GUADELOUPE', 'Guadeloupe', 'GLP', 312, 590),
(87, 'GU', 'GUAM', 'Guam', 'GUM', 316, 1671),
(88, 'GT', 'GUATEMALA', 'Guatemala', 'GTM', 320, 502),
(89, 'GN', 'GUINEA', 'Guinea', 'GIN', 324, 224),
(90, 'GW', 'GUINEA-BISSAU', 'Guinea-Bissau', 'GNB', 624, 245),
(91, 'GY', 'GUYANA', 'Guyana', 'GUY', 328, 592),
(92, 'HT', 'HAITI', 'Haiti', 'HTI', 332, 509),
(93, 'HM', 'HEARD ISLAND AND MCDONALD ISLANDS', 'Heard Island and Mcdonald Islands', NULL, NULL, 0),
(94, 'VA', 'HOLY SEE (VATICAN CITY STATE)', 'Holy See (Vatican City State)', 'VAT', 336, 39),
(95, 'HN', 'HONDURAS', 'Honduras', 'HND', 340, 504),
(96, 'HK', 'HONG KONG', 'Hong Kong', 'HKG', 344, 852),
(97, 'HU', 'HUNGARY', 'Hungary', 'HUN', 348, 36),
(98, 'IS', 'ICELAND', 'Iceland', 'ISL', 352, 354),
(99, 'IN', 'INDIA', 'India', 'IND', 356, 91),
(100, 'ID', 'INDONESIA', 'Indonesia', 'IDN', 360, 62),
(101, 'IR', 'IRAN, ISLAMIC REPUBLIC OF', 'Iran, Islamic Republic of', 'IRN', 364, 98),
(102, 'IQ', 'IRAQ', 'Iraq', 'IRQ', 368, 964),
(103, 'IE', 'IRELAND', 'Ireland', 'IRL', 372, 353),
(104, 'IL', 'ISRAEL', 'Israel', 'ISR', 376, 972),
(105, 'IT', 'ITALY', 'Italy', 'ITA', 380, 39),
(106, 'JM', 'JAMAICA', 'Jamaica', 'JAM', 388, 1876),
(107, 'JP', 'JAPAN', 'Japan', 'JPN', 392, 81),
(108, 'JO', 'JORDAN', 'Jordan', 'JOR', 400, 962),
(109, 'KZ', 'KAZAKHSTAN', 'Kazakhstan', 'KAZ', 398, 7),
(110, 'KE', 'KENYA', 'Kenya', 'KEN', 404, 254),
(111, 'KI', 'KIRIBATI', 'Kiribati', 'KIR', 296, 686),
(112, 'KP', "KOREA, DEMOCRATIC PEOPLE''S REPUBLIC OF", "Korea, Democratic People''s Republic of", 'PRK', 408, 850),
(113, 'KR', 'KOREA, REPUBLIC OF', 'Korea, Republic of', 'KOR', 410, 82),
(114, 'KW', 'KUWAIT', 'Kuwait', 'KWT', 414, 965),
(115, 'KG', 'KYRGYZSTAN', 'Kyrgyzstan', 'KGZ', 417, 996),
(116, 'LA', "LAO PEOPLE''S DEMOCRATIC REPUBLIC", "Lao People''s Democratic Republic", 'LAO', 418, 856),
(117, 'LV', 'LATVIA', 'Latvia', 'LVA', 428, 371),
(118, 'LB', 'LEBANON', 'Lebanon', 'LBN', 422, 961),
(119, 'LS', 'LESOTHO', 'Lesotho', 'LSO', 426, 266),
(120, 'LR', 'LIBERIA', 'Liberia', 'LBR', 430, 231),
(121, 'LY', 'LIBYAN ARAB JAMAHIRIYA', 'Libyan Arab Jamahiriya', 'LBY', 434, 218),
(122, 'LI', 'LIECHTENSTEIN', 'Liechtenstein', 'LIE', 438, 423),
(123, 'LT', 'LITHUANIA', 'Lithuania', 'LTU', 440, 370),
(124, 'LU', 'LUXEMBOURG', 'Luxembourg', 'LUX', 442, 352),
(125, 'MO', 'MACAO', 'Macao', 'MAC', 446, 853),
(126, 'MK', 'MACEDONIA, THE FORMER YUGOSLAV REPUBLIC OF', 'Macedonia, the Former Yugoslav Republic of', 'MKD', 807, 389),
(127, 'MG', 'MADAGASCAR', 'Madagascar', 'MDG', 450, 261),
(128, 'MW', 'MALAWI', 'Malawi', 'MWI', 454, 265),
(129, 'MY', 'MALAYSIA', 'Malaysia', 'MYS', 458, 60),
(130, 'MV', 'MALDIVES', 'Maldives', 'MDV', 462, 960),
(131, 'ML', 'MALI', 'Mali', 'MLI', 466, 223),
(132, 'MT', 'MALTA', 'Malta', 'MLT', 470, 356),
(133, 'MH', 'MARSHALL ISLANDS', 'Marshall Islands', 'MHL', 584, 692),
(134, 'MQ', 'MARTINIQUE', 'Martinique', 'MTQ', 474, 596),
(135, 'MR', 'MAURITANIA', 'Mauritania', 'MRT', 478, 222),
(136, 'MU', 'MAURITIUS', 'Mauritius', 'MUS', 480, 230),
(137, 'YT', 'MAYOTTE', 'Mayotte', NULL, NULL, 269),
(138, 'MX', 'MEXICO', 'Mexico', 'MEX', 484, 52),
(139, 'FM', 'MICRONESIA, FEDERATED STATES OF', 'Micronesia, Federated States of', 'FSM', 583, 691),
(140, 'MD', 'MOLDOVA, REPUBLIC OF', 'Moldova, Republic of', 'MDA', 498, 373),
(141, 'MC', 'MONACO', 'Monaco', 'MCO', 492, 377),
(142, 'MN', 'MONGOLIA', 'Mongolia', 'MNG', 496, 976),
(143, 'MS', 'MONTSERRAT', 'Montserrat', 'MSR', 500, 1664),
(144, 'MA', 'MOROCCO', 'Morocco', 'MAR', 504, 212),
(145, 'MZ', 'MOZAMBIQUE', 'Mozambique', 'MOZ', 508, 258),
(146, 'MM', 'MYANMAR', 'Myanmar', 'MMR', 104, 95),
(147, 'NA', 'NAMIBIA', 'Namibia', 'NAM', 516, 264),
(148, 'NR', 'NAURU', 'Nauru', 'NRU', 520, 674),
(149, 'NP', 'NEPAL', 'Nepal', 'NPL', 524, 977),
(150, 'NL', 'NETHERLANDS', 'Netherlands', 'NLD', 528, 31),
(151, 'AN', 'NETHERLANDS ANTILLES', 'Netherlands Antilles', 'ANT', 530, 599),
(152, 'NC', 'NEW CALEDONIA', 'New Caledonia', 'NCL', 540, 687),
(153, 'NZ', 'NEW ZEALAND', 'New Zealand', 'NZL', 554, 64),
(154, 'NI', 'NICARAGUA', 'Nicaragua', 'NIC', 558, 505),
(155, 'NE', 'NIGER', 'Niger', 'NER', 562, 227),
(156, 'NG', 'NIGERIA', 'Nigeria', 'NGA', 566, 234),
(157, 'NU', 'NIUE', 'Niue', 'NIU', 570, 683),
(158, 'NF', 'NORFOLK ISLAND', 'Norfolk Island', 'NFK', 574, 672),
(159, 'MP', 'NORTHERN MARIANA ISLANDS', 'Northern Mariana Islands', 'MNP', 580, 1670),
(160, 'NO', 'NORWAY', 'Norway', 'NOR', 578, 47),
(161, 'OM', 'OMAN', 'Oman', 'OMN', 512, 968),
(162, 'PK', 'PAKISTAN', 'Pakistan', 'PAK', 586, 92),
(163, 'PW', 'PALAU', 'Palau', 'PLW', 585, 680),
(164, 'PS', 'PALESTINIAN TERRITORY, OCCUPIED', 'Palestinian Territory, Occupied', NULL, NULL, 970),
(165, 'PA', 'PANAMA', 'Panama', 'PAN', 591, 507),
(166, 'PG', 'PAPUA NEW GUINEA', 'Papua New Guinea', 'PNG', 598, 675),
(167, 'PY', 'PARAGUAY', 'Paraguay', 'PRY', 600, 595),
(168, 'PE', 'PERU', 'Peru', 'PER', 604, 51),
(169, 'PH', 'PHILIPPINES', 'Philippines', 'PHL', 608, 63),
(170, 'PN', 'PITCAIRN', 'Pitcairn', 'PCN', 612, 0),
(171, 'PL', 'POLAND', 'Poland', 'POL', 616, 48),
(172, 'PT', 'PORTUGAL', 'Portugal', 'PRT', 620, 351),
(173, 'PR', 'PUERTO RICO', 'Puerto Rico', 'PRI', 630, 1787),
(174, 'QA', 'QATAR', 'Qatar', 'QAT', 634, 974),
(175, 'RE', 'REUNION', 'Reunion', 'REU', 638, 262),
(176, 'RO', 'ROMANIA', 'Romania', 'ROM', 642, 40),
(177, 'RU', 'RUSSIAN FEDERATION', 'Russian Federation', 'RUS', 643, 70),
(178, 'RW', 'RWANDA', 'Rwanda', 'RWA', 646, 250),
(179, 'SH', 'SAINT HELENA', 'Saint Helena', 'SHN', 654, 290),
(180, 'KN', 'SAINT KITTS AND NEVIS', 'Saint Kitts and Nevis', 'KNA', 659, 1869),
(181, 'LC', 'SAINT LUCIA', 'Saint Lucia', 'LCA', 662, 1758),
(182, 'PM', 'SAINT PIERRE AND MIQUELON', 'Saint Pierre and Miquelon', 'SPM', 666, 508),
(183, 'VC', 'SAINT VINCENT AND THE GRENADINES', 'Saint Vincent and the Grenadines', 'VCT', 670, 1784),
(184, 'WS', 'SAMOA', 'Samoa', 'WSM', 882, 684),
(185, 'SM', 'SAN MARINO', 'San Marino', 'SMR', 674, 378),
(186, 'ST', 'SAO TOME AND PRINCIPE', 'Sao Tome and Principe', 'STP', 678, 239),
(187, 'SA', 'SAUDI ARABIA', 'Saudi Arabia', 'SAU', 682, 966),
(188, 'SN', 'SENEGAL', 'Senegal', 'SEN', 686, 221),
(189, 'CS', 'SERBIA AND MONTENEGRO', 'Serbia and Montenegro', NULL, NULL, 381),
(190, 'SC', 'SEYCHELLES', 'Seychelles', 'SYC', 690, 248),
(191, 'SL', 'SIERRA LEONE', 'Sierra Leone', 'SLE', 694, 232),
(192, 'SG', 'SINGAPORE', 'Singapore', 'SGP', 702, 65),
(193, 'SK', 'SLOVAKIA', 'Slovakia', 'SVK', 703, 421),
(194, 'SI', 'SLOVENIA', 'Slovenia', 'SVN', 705, 386),
(195, 'SB', 'SOLOMON ISLANDS', 'Solomon Islands', 'SLB', 90, 677),
(196, 'SO', 'SOMALIA', 'Somalia', 'SOM', 706, 252),
(197, 'ZA', 'SOUTH AFRICA', 'South Africa', 'ZAF', 710, 27),
(198, 'GS', 'SOUTH GEORGIA AND THE SOUTH SANDWICH ISLANDS', 'South Georgia and the South Sandwich Islands', NULL, NULL, 0),
(199, 'ES', 'SPAIN', 'Spain', 'ESP', 724, 34),
(200, 'LK', 'SRI LANKA', 'Sri Lanka', 'LKA', 144, 94),
(201, 'SD', 'SUDAN', 'Sudan', 'SDN', 736, 249),
(202, 'SR', 'SURINAME', 'Suriname', 'SUR', 740, 597),
(203, 'SJ', 'SVALBARD AND JAN MAYEN', 'Svalbard and Jan Mayen', 'SJM', 744, 47),
(204, 'SZ', 'SWAZILAND', 'Swaziland', 'SWZ', 748, 268),
(205, 'SE', 'SWEDEN', 'Sweden', 'SWE', 752, 46),
(206, 'CH', 'SWITZERLAND', 'Switzerland', 'CHE', 756, 41),
(207, 'SY', 'SYRIAN ARAB REPUBLIC', 'Syrian Arab Republic', 'SYR', 760, 963),
(208, 'TW', 'TAIWAN, PROVINCE OF CHINA', 'Taiwan, Province of China', 'TWN', 158, 886),
(209, 'TJ', 'TAJIKISTAN', 'Tajikistan', 'TJK', 762, 992),
(210, 'TZ', 'TANZANIA, UNITED REPUBLIC OF', 'Tanzania, United Republic of', 'TZA', 834, 255),
(211, 'TH', 'THAILAND', 'Thailand', 'THA', 764, 66),
(212, 'TL', 'TIMOR-LESTE', 'Timor-Leste', NULL, NULL, 670),
(213, 'TG', 'TOGO', 'Togo', 'TGO', 768, 228),
(214, 'TK', 'TOKELAU', 'Tokelau', 'TKL', 772, 690),
(215, 'TO', 'TONGA', 'Tonga', 'TON', 776, 676),
(216, 'TT', 'TRINIDAD AND TOBAGO', 'Trinidad and Tobago', 'TTO', 780, 1868),
(217, 'TN', 'TUNISIA', 'Tunisia', 'TUN', 788, 216),
(218, 'TR', 'TURKEY', 'Turkey', 'TUR', 792, 90),
(219, 'TM', 'TURKMENISTAN', 'Turkmenistan', 'TKM', 795, 7370),
(220, 'TC', 'TURKS AND CAICOS ISLANDS', 'Turks and Caicos Islands', 'TCA', 796, 1649),
(221, 'TV', 'TUVALU', 'Tuvalu', 'TUV', 798, 688),
(222, 'UG', 'UGANDA', 'Uganda', 'UGA', 800, 256),
(223, 'UA', 'UKRAINE', 'Ukraine', 'UKR', 804, 380),
(224, 'AE', 'UNITED ARAB EMIRATES', 'United Arab Emirates', 'ARE', 784, 971),
(225, 'GB', 'UNITED KINGDOM', 'United Kingdom', 'GBR', 826, 44),
(226, 'US', 'UNITED STATES', 'United States', 'USA', 840, 1),
(227, 'UM', 'UNITED STATES MINOR OUTLYING ISLANDS', 'United States Minor Outlying Islands', NULL, NULL, 1),
(228, 'UY', 'URUGUAY', 'Uruguay', 'URY', 858, 598),
(229, 'UZ', 'UZBEKISTAN', 'Uzbekistan', 'UZB', 860, 998),
(230, 'VU', 'VANUATU', 'Vanuatu', 'VUT', 548, 678),
(231, 'VE', 'VENEZUELA', 'Venezuela', 'VEN', 862, 58),
(232, 'VN', 'VIET NAM', 'Viet Nam', 'VNM', 704, 84),
(233, 'VG', 'VIRGIN ISLANDS, BRITISH', 'Virgin Islands, British', 'VGB', 92, 1284),
(234, 'VI', 'VIRGIN ISLANDS, U.S.', 'Virgin Islands, U.s.', 'VIR', 850, 1340),
(235, 'WF', 'WALLIS AND FUTUNA', 'Wallis and Futuna', 'WLF', 876, 681),
(236, 'EH', 'WESTERN SAHARA', 'Western Sahara', 'ESH', 732, 212),
(237, 'YE', 'YEMEN', 'Yemen', 'YEM', 887, 967),
(238, 'ZM', 'ZAMBIA', 'Zambia', 'ZMB', 894, 260),
(239, 'ZW', 'ZIMBABWE', 'Zimbabwe', 'ZWE', 716, 263);
```

# DBT
## create the folder ```models/sources```

- create sources.yml inside of it:
```
# sources.yml
version: 2

sources:
  - name: retail
    database: airtube-390719 # Put the project id!

    tables:
      - name: raw_invoices
			- name: country
```

- create ```models/transform```:

And add all of the following DIM's and Fact Tables:

- dim_customer.sql:
```
-- dim_customer.sql

-- Create the dimension table
WITH customer_cte AS (
	SELECT DISTINCT
	    {{ dbt_utils.generate_surrogate_key(['CustomerID', 'Country']) }} as customer_id,
	    Country AS country
	FROM {{ source('retail', 'raw_invoices') }}
	WHERE CustomerID IS NOT NULL
)
SELECT
    t.*,
	cm.iso
FROM customer_cte t
LEFT JOIN {{ source('retail', 'country') }} cm ON t.country = cm.nicename
```
- dim_datetime.sql:
```
-- dim_datetime.sql

-- Create a CTE to extract date and time components
WITH datetime_cte AS (  
  SELECT DISTINCT
    InvoiceDate AS datetime_id,
    CASE
      WHEN LENGTH(InvoiceDate) = 16 THEN
        -- Date format: "DD/MM/YYYY HH:MM"
        PARSE_DATETIME('%m/%d/%Y %H:%M', InvoiceDate)
      WHEN LENGTH(InvoiceDate) <= 14 THEN
        -- Date format: "MM/DD/YY HH:MM"
        PARSE_DATETIME('%m/%d/%y %H:%M', InvoiceDate)
      ELSE
        NULL
    END AS date_part,
  FROM {{ source('retail', 'raw_invoices') }}
  WHERE InvoiceDate IS NOT NULL
)
SELECT
  datetime_id,
  date_part as datetime,
  EXTRACT(YEAR FROM date_part) AS year,
  EXTRACT(MONTH FROM date_part) AS month,
  EXTRACT(DAY FROM date_part) AS day,
  EXTRACT(HOUR FROM date_part) AS hour,
  EXTRACT(MINUTE FROM date_part) AS minute,
  EXTRACT(DAYOFWEEK FROM date_part) AS weekday
FROM datetime_cte
```

- dim_product.sql:
```
-- dim_product.sql
-- StockCode isn't unique, a product with the same id can have different and prices
-- Create the dimension table
SELECT DISTINCT
    {{ dbt_utils.generate_surrogate_key(['StockCode', 'Description', 'UnitPrice']) }} as product_id,
		StockCode AS stock_code,
    Description AS description,
    UnitPrice AS price
FROM {{ source('retail', 'raw_invoices') }}
WHERE StockCode IS NOT NULL
AND UnitPrice > 0
```

- fct_invoices.sql:
```
-- fct_invoices.sql

-- Create the fact table by joining the relevant keys from dimension table
WITH fct_invoices_cte AS (
    SELECT
        InvoiceNo AS invoice_id,
        InvoiceDate AS datetime_id,
        {{ dbt_utils.generate_surrogate_key(['StockCode', 'Description', 'UnitPrice']) }} as product_id,
        {{ dbt_utils.generate_surrogate_key(['CustomerID', 'Country']) }} as customer_id,
        Quantity AS quantity,
        Quantity * UnitPrice AS total
    FROM {{ source('retail', 'raw_invoices') }}
    WHERE Quantity > 0
)
SELECT
    invoice_id,
    dt.datetime_id,
    dp.product_id,
    dc.customer_id,
    quantity,
    total
FROM fct_invoices_cte fi
INNER JOIN {{ ref('dim_datetime') }} dt ON fi.datetime_id = dt.datetime_id
INNER JOIN {{ ref('dim_product') }} dp ON fi.product_id = dp.product_id
INNER JOIN {{ ref('dim_customer') }} dc ON fi.customer_id = dc.customer_id
```

## Run the  DBT models to create these tables:
```
astro dev bash
source /usr/local/airflow/dbt_venv/bin/activate
cd include/dbt 
dbt deps
dbt run --profiles-dir /usr/local/airflow/include/dbt/
```
dbt deps : install all the dependencies, watch out to not commit those files, add a .gitignore for them.

- look to the terminal and see if the models were created succesfully:
![DBTModels](https://github.com/matheusbudin/airflow-bq-dbt-soda/blob/main/images/dbt%20models%20deployed%20succesfully.png)




After succesfully executing the models, go on big query and see if the tables were created:


![BigqueryTables](https://github.com/matheusbudin/airflow-bq-dbt-soda/blob/main/images/big%20query%20facts%20and%20dimention%20tables.png)

## back to your dag
- Add the task:
```
from include.dbt.cosmos_config import DBT_PROJECT_CONFIG, DBT_CONFIG
from cosmos.airflow.task_group import DbtTaskGroup
from cosmos.constants import LoadMode
from cosmos.config import ProjectConfig, RenderConfig

transform = DbtTaskGroup(
        group_id='transform',
        project_config=DBT_PROJECT_CONFIG,
        profile_config=DBT_CONFIG,
        render_config=RenderConfig(
            load_method=LoadMode.DBT_LS,
            select=['path:models/transform']
        )
    )
```

- Create a DBT config file:
```
# include/dbt/cosmos_config.py

from cosmos.config import ProfileConfig, ProjectConfig
from pathlib import Path

DBT_CONFIG = ProfileConfig(
    profile_name='retail',
    target_name='dev',
    profiles_yml_filepath=Path('/usr/local/airflow/include/dbt/profiles.yml')
)

DBT_PROJECT_CONFIG = ProjectConfig(
    dbt_project_path='/usr/local/airflow/include/dbt/',
)
```
- test your task:
```
astro dev bash
airflow tasks list retail
airflow tasks test retail transform.dim_customer.dim_customer_run 2023-01-01
airflow tasks test retail transform.dim_customer.dim_customer_test 2023-01-01
```

## Now you can go to your airflow UI and check that Cosmos have worked, you will see a expandable task:


![CosmosAirflow](https://github.com/matheusbudin/airflow-bq-dbt-soda/blob/main/images/pipeline%20built%20airflow.png)

# Soda data quality testing for the DBT Models:

## In the directory: ```include/soda/checks/transform``` include:

- dim_customer.yml
```
# dim_customer.yml
checks for dim_customer:
  - schema:
      fail:
        when required column missing: 
          [customer_id, country]
        when wrong column type:
          customer_id: string
          country: string
  - duplicate_count(customer_id) = 0:
      name: All customers are unique
  - missing_count(customer_id) = 0:
      name: All customers have a key
```
- dim_datetime.yml
```
# dim_datetime.yml
checks for dim_datetime:
  # Check fails when product_key or english_product_name is missing, OR
  # when the data type of those columns is other than specified
  - schema:
      fail:
        when required column missing: [datetime_id, datetime]
        when wrong column type:
          datetime_id: string
          datetime: datetime
  # Check failes when weekday is not in range 0-6
  - invalid_count(weekday) = 0:
      name: All weekdays are in range 0-6
      valid min: 0
      valid max: 6
  # Check fails when customer_id is not unique
  - duplicate_count(datetime_id) = 0:
      name: All datetimes are unique
  # Check fails when any NULL values exist in the column
  - missing_count(datetime_id) = 0:
      name: All datetimes have a key
```

- dim_product.yml:
```
# dim_product.yml
checks for dim_product:
  # Check fails when product_key or english_product_name is missing, OR
  # when the data type of those columns is other than specified
  - schema:
      fail:
        when required column missing: [product_id, description, price]
        when wrong column type:
          product_id: string
          description: string
          price: float64
  # Check fails when customer_id is not unique
  - duplicate_count(product_id) = 0:
      name: All products are unique
  # Check fails when any NULL values exist in the column
  - missing_count(product_id) = 0:
      name: All products have a key
  # Check fails when any prices are negative
  - min(price):
      fail: when < 0
```
- fct_invoices.yml:
```
# fct_invoices.yml
checks for fct_invoices:
  # Check fails when invoice_id, quantity, total is missing or
  # when the data type of those columns is other than specified
  - schema:
      fail:
        when required column missing: 
          [invoice_id, product_id, customer_id, datetime_id, quantity, total]
        when wrong column type:
          invoice_id: string
          product_id: string
          customer_id: string
          datetime_id: string
          quantity: int
          total: float64
  # Check fails when NULL values in the column
  - missing_count(invoice_id) = 0:
      name: All invoices have a key
  # Check fails when the total of any invoices is negative
  - failed rows:
      name: All invoices have a positive total amount
      fail query: |
        SELECT invoice_id, total
        FROM fct_invoices
        WHERE total < 0
```

## Add a new task in your dag:
```
@task.external_python(python='/usr/local/airflow/soda_venv/bin/python')
    def check_transform(scan_name='check_transform', checks_subpath='transform'):
        from include.soda.check_function import check

        return check(scan_name, checks_subpath)
```

# Finally we are going to create the reports tables, that will be consumed by Power bi:

## Create the folder: ```include/dbt/models/report ```

- report_customer_invoices.sql:
```
-- report_customer_invoices.sql
SELECT
  c.country,
  c.iso,
  COUNT(fi.invoice_id) AS total_invoices,
  SUM(fi.total) AS total_revenue
FROM {{ ref('fct_invoices') }} fi
JOIN {{ ref('dim_customer') }} c ON fi.customer_id = c.customer_id
GROUP BY c.country, c.iso
ORDER BY total_revenue DESC
LIMIT 10
```
- report_product_invoices.sql:

```
-- report_product_invoices.sql
SELECT
  p.product_id,
  p.stock_code,
  p.description,
  SUM(fi.quantity) AS total_quantity_sold
FROM {{ ref('fct_invoices') }} fi
JOIN {{ ref('dim_product') }} p ON fi.product_id = p.product_id
GROUP BY p.product_id, p.stock_code, p.description
ORDER BY total_quantity_sold DESC
LIMIT 10
```
- report_year_invoices.sql:

```
-- report_year_invoices.sql
SELECT
  dt.year,
  dt.month,
  COUNT(DISTINCT fi.invoice_id) AS num_invoices,
  SUM(fi.total) AS total_revenue
FROM {{ ref('fct_invoices') }} fi
JOIN {{ ref('dim_datetime') }} dt ON fi.datetime_id = dt.datetime_id
GROUP BY dt.year, dt.month
ORDER BY dt.year, dt.month
```
## Add a new task in your dag:
```
report = DbtTaskGroup(
        group_id='report',
        project_config=DBT_PROJECT_CONFIG,
        profile_config=DBT_CONFIG,
        render_config=RenderConfig(
            load_method=LoadMode.DBT_LS,
            select=['path:models/report']
        )
    )
```

- Test it:
```
astro dev bash
cd include/dbt
source dbt_venv/bin/activate
cd include/dbt 
dbt run --select path:models/report --profiles-dir /usr/local/airflow/include/dbt/
```

# Create data quality checks for those new DBT models:
## create the folder report: ```include/soda/checks/report```
- report_customer_invoices.yml:
```
# report_customer_invoices.yml
checks for report_customer_invoices:
  # Check fails if the country column has any missing values
  - missing_count(country) = 0:
      name: All customers have a country
  # Check fails if the total invoices is lower or equal to 0
  - min(total_invoices):
      fail: when <= 0
```
- report_product_invoices.yml:
```
# report_product_invoices.yml
checks for report_product_invoices:
  # Check fails if the stock_code column has any missing values
  - missing_count(stock_code) = 0:
      name: All products have a stock code
  # Check fails if the total quanity sold is lower or equal to 0
  - min(total_quantity_sold):
      fail: when <= 0
```
- report_year_invoices.yml:
```
# report_year_invoices.yml
checks for report_year_invoices:
  # Check fails if the number of invoices for a year is negative
  - min(num_invoices):
      fail: when < 0
```
Test your quality tests:
```
cd /usr/local/airflow
source /usr/local/airflow/soda_venv/bin/activate
soda scan -d retail -c include/soda/configuration.yml include/soda/checks/report/*
```

# Added one last task into your dag:
```
@task.external_python(python='/usr/local/airflow/soda_venv/bin/python')
    def check_report(scan_name='check_report', checks_subpath='report'):
        from include.soda.check_function import check

        return check(scan_name, checks_subpath)
```

# Finally we should be able to create a dashboard in your BI tool of preference, i am using power bi, that has a native connector to big query, all you have to do is authenticate with login and MFA and it will be connected.

## dashboard:


![dashboard](https://github.com/matheusbudin/airflow-bq-dbt-soda/blob/main/images/final%20dashborad.png)

## Future TO-DOs:
- do the same project with a more complex and dirty raw data set, to perform data cleaning;
- use Snowflake instead of big query to test airflow connectors for Snowflake.
