"""helper functions to load movielens data"""
import csv
import urllib
import zipfile


def create_table(connection, tablequery):
    """create a table from a query

    arguments:
    connection -- a postgresql connection object
    tablequery -- the sql string to create the table
    """
    cur = connection.cursor()
    cur.execute(tablequery)
    connection.commit()


def load_data(connection, insert_sql, data):
    """load a table with data

    arguments:
    connection -- a postgresql connection object
    insert_sql -- an sql string for inserting a row in the table
    data -- a list of entries to insert per row
    """
    cur = connection.cursor()
    for d in data:
        cur.execute(insert_sql, d)
    connection.commit()


def get_data_from_file(csvfile):
    """return the data from a csvfile as a list, without header line

    arguments:
    csvfile -- the path of csvfile to load
    """
    with open(csvfile) as cf:
        reader = csv.reader(cf, delimiter=',', quotechar='"')
        data = [row for row in reader][1:]
    return data


def create_products_table(connection):
    """create the products table

    arguments:
    connection -- a postgresql connection object
    """
    table_sql = 'create table ' \
                'products(id integer, description text, genres text)'
    create_table(connection, table_sql)


def load_products_data(connection, csvfile):
    """load data into the products table

    arguments:
    connection -- a postgresql connection object
    csvfile -- the path of csvfile to load
    """
    insert_sql = 'insert into products (id, description, genres) ' \
                 'values (%s, %s, %s)'
    load_data(connection, insert_sql, get_data_from_file(csvfile))


def create_ratings_table(connection):
    """create the ratings table

    arguments:
    connection -- a postgresql connection object
    """
    table_sql = 'create table ' \
                'ratings(id serial primary key, userId integer, movieId integer, ' \
                'rating real, timestamp integer) '
    create_table(connection, table_sql)


def load_ratings_data(connection, csvfile):
    """load data into the ratings table

    arguments:
    connection -- a postgresql connection object
    csvfile -- the path of csvfile to load
    """
    insert_sql = 'insert into ratings (userId, movieId, rating, timestamp) ' \
                 'values (%s, %s, %s, %s)'
    load_data(connection, insert_sql, get_data_from_file(csvfile))


def download_and_unzip_dataset(url, path):
    """download the movielens data and unzip it

    arguments:
    url -- the url to download from
    path -- the path to unzip the files into
    """
    dl = urllib.urlretrieve(url)
    zf = zipfile.ZipFile(dl[0])
    zf.extractall(path)
    return zf
