## Introduction
```
'AIMS' is an console application for managing accidents happened in a company
it consist of three roles:

1. Admin
2. Supervisor 
3. Employee

```

Activate your Python virtual environment, and download the required libraries
```
source venv/bin/activate
export PYTHONPATH = '.'
pip install -r requirements.txt
```

## How to run app on local laptop

Follow the guide here to ensure you run correct main file
```
'python aims/login.py'

after above command login menu will be shown:
then use up/down arrow keys to navigate and
use 'enter' key to select any option

```

To connect to your local sqlite: 

```
MGNREGA> cd data
MGNREGA/data>  sqlite3 aims.db
MGNREGA/data> select * from <your_table> (or describe <your_table>)
```
```
Database schema is created once via the file `data/schema_script.sql`
```


Key Entities in Code
----
```   
+-- common
|  +--connect_db.py
|  +--constants.py
|  +--helper.py
|  +--password_encryption.py
|  +--validations.py

+-- data
|  +--aims.db
|  +--schema_script.sql

+-- aims
|  +--admin.py
|  +--config.yaml
|  +--employee.py
|  +--login.py
|  +--supervisor.py

 
```
Other Entities for data analytics
----
```
CSVs ->
        contains analytics csv
Resuls->
        contins pdfs of graphs created using above 
        analytics csv
test -> 
        contains unit testing code
htmlcov->
        contains coverage for above code
    
```