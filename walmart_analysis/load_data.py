import csv
import psycopg2

from walmart_analysis.settings import logger


def create_table(psql_conn):
    q = """
    CREATE TABLE IF NOT EXISTS walmart_sales (
        invoice_id VARCHAR(30) NOT NULL,
        branch VARCHAR(5) NOT NULL,
        city VARCHAR(30) NOT NULL,
        customer_type VARCHAR(30) NOT NULL,
        gender VARCHAR(10) NOT NULL,
        product_line VARCHAR(100) NOT NULL,
        unit_price numeric(10,2) NOT NULL,
        quantity INT NOT NULL,
        tax numeric(6,4) NOT NULL,
        total numeric(10,4) NOT NULL,
        cur_date DATE NOT null DEFAULT CURRENT_DATE,
        cur_time TIME NOT null DEFAULT CURRENT_TIME,
        payment VARCHAR(30) NOT NULL,
        cogs numeric(10,2) NOT NULL,
        gross_margin_percentage NUMERIC(11,9) NOT NULL,
        gross_income NUMERIC(10,4) NOT NULL,
        rating numeric(3,1) NOT NULL
);
    """
    try:
        cur = psql_conn.cursor()

        cur.execute(q)
        logger.info(f'Creating table')
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
                    cur_date,
                    cur_time,
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
                    row.get('Invoice_ID', ''), row['Branch'], row['City'],
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
