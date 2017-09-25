# MTC-import

Python script to import Monthly Treatment Completeness data from a CSV into Bahmni

## Running the script
1. It is much easier to manage multiple sets of Python dependencies using [Virtual Environments](http://docs.python-guide.org/en/latest/dev/virtualenvs/).
1. Install Python dependencies for production.

    `pip install -r requirements.txt`

1. Run the script.

    `python mtc_import/import_mtc_data.py <FILEPATH> <API_USERNAME> <API_PASSWORD> <API_URL>`

## Running the tests
1. Install Python dependencies for development.

    `pip install -r requirements_dev.txt`

1. Run the tests.

    `py.test`
