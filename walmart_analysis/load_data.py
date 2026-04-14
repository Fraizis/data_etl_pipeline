import csv
import json

import pandas
import psycopg2
from psycopg2 import sql

from walmart_analysis.settings import logger, CSV_FILE, JSON_FILE


def create_table(psql_conn):
    q = """
    CREATE TABLE IF NOT EXISTS walmart_sales (
        invoice_id VARCHAR(30),
        branch VARCHAR(10),
        city VARCHAR(30),
        customer_type VARCHAR(30),
        gender VARCHAR(10),
        product_line VARCHAR(100),
        unit_price TEXT,
        quantity INT,
        tax NUMERIC,
        total NUMERIC,
        date DATE DEFAULT CURRENT_DATE,
        time TIME DEFAULT CURRENT_TIME,
        payment VARCHAR(30),
        cogs NUMERIC,
        gross_margin_percentage NUMERIC,
        gross_income NUMERIC,
        rating NUMERIC
    );
    """
    try:
        cur = psql_conn.cursor()

        cur.execute(q)
        logger.info(f'Executed query: {q}')
        cur.close()
        psql_conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)


def save_to_db(conn, file):
    q = f"""
    INSERT INTO walmart_sales (
                    invoice_id,
                    branch,
                    City,
                    Customer_type,
                    Gender,
                    Product_line,
                    Unit_price,
                    Quantity,
                    Tax,
                    Total,
                    Date,
                    Time,
                    Payment,
                    cogs,
                    gross_margin_percentage,
                    gross_income,
                    Rating
                    )
                    values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    try:
        logger.info('Saving data to postgres')

        cur = conn.cursor()

        with open(file, 'r') as csvfile:
            csv_reader = csv.DictReader(csvfile)
            s = [
                (
                    row['Invoice_ID'], row['Branch'], row['City'],
                    row['Customer_type'], row['Gender'], row['Product_line'],
                    row['Unit_price'], row['Quantity'], row['Tax_5%'],
                    row['Total'], row['Date'], row['Time'],
                    row['Payment'], row['cogs'], row['gross_margin_percentage'],
                    row['gross_income'], row['Rating']
                ) for row in csv_reader
            ]
        logger.info(f'Executed query: {q}')
        cur.executemany(q, s)
        conn.commit()

        cur.close()
        logger.info('Done')

    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)
