import psycopg2

from walmart_analysis.settings import logger

day_time = """
alter table walmart_sales add column IF NOT EXISTS time_of_day VARCHAR(20);

update walmart_sales
set time_of_day = (
	case 
		when cur_time >= '10:00:00' and cur_time <= '12:00:00' then 'Morning'
		when cur_time > '12:00:00' and cur_time <= '18:00:00' then 'Afternoon'
		when cur_time > '18:00:00' and cur_time <= '21:00:00' then 'Evening'
	end
);
"""

day_name = """
alter table walmart_sales add column IF NOT EXISTS day_name VARCHAR(20);

update walmart_sales
set day_name = (
    TO_CHAR(cur_date, 'Dy')
);
"""

month_name = """
alter table walmart_sales add column IF NOT EXISTS month_name VARCHAR(20);

update walmart_sales
set month_name = (
    TO_CHAR(cur_date, 'Mon')
);
"""


def add_time_day_month(conn):
    try:
        cur = conn.cursor()

        cur.execute(day_time)
        cur.execute(day_name)
        cur.execute(month_name)

        conn.commit()

        cur.close()
        logger.info('Added columns day_time, day_name, month_name')

    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)
