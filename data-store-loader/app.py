#!/usr/bin/env python
import argparse
import logging
import os
import os.path
import sys

import psycopg2

import movielens


def make_connection(host='127.0.0.1', port=5432, user='postgres',
                    password='postgres', dbname='postgres'):
    return psycopg2.connect(host=host, port=port, user=user,
                            password=password, dbname=dbname)


def build_connection(args):
    """make the db connection with an args object"""
    conn = make_connection(host=args.host,
                           port=args.port,
                           user=args.user,
                           password=args.password,
                           dbname=args.dbname)
    return conn


def parse_args(parser):
    args = parser.parse_args()
    args.host = os.getenv('DB_HOST', args.host)
    args.port = os.getenv('DB_PORT', args.port)
    args.user = os.getenv('DB_USER', args.user)
    args.password = os.getenv('DB_PASSWORD', args.password)
    args.dbname = os.getenv('DB_DBNAME', args.dbname)
    args.movies = os.getenv('MOVIES_CSV', args.movies)
    args.ratings = os.getenv('RATINGS_CSV', args.ratings)
    args.dataset = os.getenv('DATASET_URL', args.dataset)
    return args


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logging.info('starting data loader')
    parser = argparse.ArgumentParser(description='load a data store')
    parser.add_argument(
        '--host', default='127.0.0.1',
        help='the postgresql host address (default: 127.0.0.1). '
        'env variable: DB_HOST')
    parser.add_argument(
        '--port', default=5432, help='the postgresql port (default: 5432). '
        'env variable: DB_PORT')
    parser.add_argument(
        '--user', default='postgres',
        help='the user for the postgresql database (default: postgres). '
        'env variable: DB_USER')
    parser.add_argument(
        '--password', default='postgres',
        help='the password for the postgresql user (default: postgres). '
        'env variable: DB_PASSWORD')
    parser.add_argument(
        '--dbname', default='postgres',
        help='the database name to load with data. env variable: DB_DBNAME')
    parser.add_argument(
        '--movies', required=False,
        help='path to the movies.csv file from the movielens'
        ' dataset. env variable: MOVIES_CSV')
    parser.add_argument(
        '--ratings', required=False,
        help='path to the ratings.csv file from the movielens'
        ' dataset. env variable: RATINGS_CSV')
    parser.add_argument(
        '--dataset', required=False,
        help='url of a dataset to download and extract, this will override '
        '--ratings and --movies settings. env variable: DATASET_URL')
    args = parse_args(parser)

    if args.movies is None and args.ratings is None and args.dataset is None:
        logging.error('no csv files or dataset url specified')
        sys.exit(1)

    logging.info('connecting to database')
    conn = build_connection(args)

    logging.info('creating products table')
    try:
        movielens.create_products_table(conn)
    except psycopg2.ProgrammingError:
        logging.warning('products table exists')
        conn.close()
        conn = build_connection(args)

    logging.info('creating ratings table')
    try:
        movielens.create_ratings_table(conn)
    except psycopg2.ProgrammingError:
        logging.warning('ratings table exists')
        conn.close()
        conn = build_connection(args)

    if args.movies is not None:
        movies_csv = args.movies
    else:
        movies_csv = None
    if args.ratings is not None:
        ratings_csv = args.ratings
    else:
        ratings_csv = None

    if args.dataset is not None:
        uz_path = '/tmp'
        logging.info('downloading and unzipping dataset')
        zfiles = movielens.download_and_unzip_dataset(args.dataset, uz_path)
        for f in zfiles.filelist:
            if f.filename.endswith('movies.csv'):
                logging.info('found movies.csv file in dataset')
                movies_csv = os.path.join(uz_path, f.filename)
            elif f.filename.endswith('ratings.csv'):
                logging.info('found ratings.csv file in dataset')
                ratings_csv = os.path.join(uz_path, f.filename)

    if movies_csv is not None:
        logging.info('loading products table')
        movielens.load_products_data(conn, movies_csv)

    if ratings_csv is not None:
        logging.info('loading ratings table')
        movielens.load_ratings_data(conn, ratings_csv)
