from prepare_connection import (
    init_logger,
    psql_connection,
    create_table,
    etl_pipeline
)

if __name__ == '__main__':
    init_logger()
    conn = psql_connection()
    create_table(conn)
    etl_pipeline('2020.csv', conn)
