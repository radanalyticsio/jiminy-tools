# Data Store Loader

This directory contains python modules designed to speed the process of
loading data into a PostgreSQL database for later usage by the Jiminy project.

## Quickstart

The easiest way to utilize these modules for loading a database is by
creating a virtual environment using the
[virtualenv](https://pypi.python.org/pypi/virtualenv) tool.

after activating the virtual environment, you will need to install the
requirements for this tool by running the following:

    pip install -r requirements.txt

with a postgresql database running you can now load the movielens csv files.
here is an example:

    ./app.py --host 127.0.0.1 --port 5432 --user bob --password secret \
        --movies /home/me/ml-latest/movies.csv \
        --ratings /home/me/ml-latest/ratings.csv

this will spew some logging information about what is happening and eventually
your database will be loaded.

for more information about the options and defaults run this:

    ./app.py -h


**WARNING: the ratings files can be quite large and will take time to load,
    like 10-15 minutes**

## Files

### app.py

The main file for running the load process from the command line, also
contains a helper function for connecting to the database.

### movielens.py

This file contains the movielens specific functions for downloading,
unpacking, creating tables and loading data from the upstream sources.
