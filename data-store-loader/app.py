#!/usr/bin/env python
import argparse
import logging
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


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logging.info('starting data loader')
    parser = argparse.ArgumentParser(description='load a data store')
    parser.add_argument(
        '--host', default='127.0.0.1',
        help='the postgresql host address (default: 127.0.0.1)')
    parser.add_argument(
        '--port', default=5432, help='the postgresql port (default: 5432)')
    parser.add_argument(
        '--user', default='postgres',
        help='the user for the postgresql database (default: postgres)')
    parser.add_argument('--password', default='postgres',
                        help='the password for the postgresql user')
    parser.add_argument('--dbname', default='postgres',
                        help='the database name to load with data')
    parser.add_argument('--movies', required=False,
                        help='path to the movies.csv file from the movielens'
                        ' dataset')
    parser.add_argument('--ratings', required=False,
                        help='path to the ratings.csv file from the movielens'
                        ' dataset')
    args = parser.parse_args()

    if args.movies is None and args.ratings is None:
        logging.error('no csv files specified')
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
        logging.info('loading products table')
        movielens.load_products_data(conn, args.movies)

    if args.ratings is not None:
        logging.info('loading ratings table')
        movielens.load_ratings_data(conn, args.ratings)
