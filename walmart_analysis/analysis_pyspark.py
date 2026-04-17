from pyspark.sql import SparkSession

from walmart_analysis.settings import logger


def pyspark_analitics(path_to_jar, user, host, db_name, password):
    logger.info(f'Building spark session...')

    spark = (
        SparkSession.builder.
        appName("PostgreSQL Connection").
        config("spark.jars", path_to_jar).
        getOrCreate()
    )

    url = f"jdbc:postgresql://{host}:5432/{db_name}"

    properties = {
        "user": user,
        "password": password,
        "driver": "org.postgresql.Driver"
    }

    table_name = "walmart_sales"

    logger.info(f'Spark read jdbc: {url}, {table_name}')

    df = spark.read.jdbc(url=url, table=table_name, properties=properties)

    logger.info(f'Creating or replacing temp view')

    df.createOrReplaceTempView("walmart_analysis")

    # How many unique cities does the data have?
    unique_cities = """
        select distinct City as unique_cities
        from walmart_analysis;
    """

    spark.sql(unique_cities).show()
    logger.info(f'Executed unique_cities')

    # In which city is each branch?
    branch_city = """
        select distinct Branch, City
        from walmart_analysis;
    """
    spark.sql(branch_city).show()
    logger.info(f'Executed branch_city')

    # How many unique product lines does the data have?
    unique_product_lines = """
        select distinct Product_line
        from walmart_analysis;
    """
    spark.sql(unique_product_lines).show()
    logger.info(f'Executed unique_product_lines')

    # What is the most common payment method?
    common_payment_method = """
        select Payment, count(Payment) as count
        from walmart_analysis
        group by Payment
        order by count DESC;
    """
    spark.sql(common_payment_method).show()
    logger.info(f'Executed common_payment_method')

    # What is the most selling product line?
    selling_product_line = """
        select Payment, count(Payment) as count
        from walmart_analysis
        group by Payment
        order by count DESC;
    """
    spark.sql(selling_product_line).show()
    logger.info(f'Executed selling_product_line')

    # --What is the most selling product line?
    customers_most_buy = """
        select 
            Product_line as most_selling_product_line, 
            sum(quantity) as sold
        from walmart_analysis
        group by Product_line
        order by sold desc;
    """
    spark.sql(customers_most_buy).show()
    logger.info(f'Executed customers_most_buy')

    # What is the total revenue by month?
    month_revenue = """ 
        select Product_line, month_name, sum(total) as total_revenue
        from walmart_analysis
        group by Product_line, month_name
        order by Product_line;
    """
    spark.sql(month_revenue).show()
    logger.info(f'Executed month_revenue')

    # --What month had the largest COGS?
    month_cogs = """
        select month_name, sum(cogs) as largest_COGS
        from walmart_analysis
        group by month_name
        order by largest_COGS desc;
    """
    spark.sql(month_cogs).show()
    logger.info(f'Executed month_cogs')

    # --What product line had the largest revenue?
    product_revenue = """
        select Product_line, sum(total) as product_total_revenue
        from walmart_analysis
        group by Product_line
        order by product_total_revenue desc;
    """
    spark.sql(product_revenue).show()
    logger.info(f'Executed product_revenue')

    # What is the city with the largest revenue?
    city_revenue = """
    select City, sum(total) as total_revenue
    from walmart_analysis
    group by City
    order by total_revenue desc;
    """
    spark.sql(city_revenue).show()
    logger.info(f'Executed city_revenue')

    # --What product line had the largest VAT?
    product_vat = """
        select product_line, max(tax) as largest_vat
        from walmart_analysis
        group by product_line
        order by largest_vat desc;
    """
    spark.sql(product_vat).show()
    logger.info(f'Executed product_vat')

    # --Fetch each product line and add a column to those product line showing "Good", "Bad".
    # --Good if its greater than average sales
    product_greater_avg_sales = """
    with ct1 as (
        select avg(quantity) as total_average 
        from walmart_analysis
    )
    select 
        product_line, 
        avg(quantity) as avg_quantity,
        total_average,
        case
            when avg(quantity) > total_average then 'Good'
            else 'Bad'
        end as sales
    from walmart_analysis, ct1
    group by product_line, total_average;
    """
    spark.sql(product_greater_avg_sales).show()
    logger.info(f'Executed product_greater_avg_sales')

    # --Which branch sold more products than average product sold?
    brunch_more_avg_sold = """
    select branch, sum(quantity) as total_sold
    from walmart_analysis
    group by branch
    having 
        sum(quantity) > (
            select avg(quantity) total_avg 
            from walmart_analysis
    );
    """
    spark.sql(brunch_more_avg_sold).show()
    logger.info(f'Executed brunch_more_avg_sold')

    # --What is the most common product line by gender?
    common_product = """
        select gender, count(product_line) as cnt, product_line
        from walmart_analysis
        group by gender, product_line
        order by cnt desc;
    """
    spark.sql(common_product).show()
    logger.info(f'Executed common_product')

    # --What is the average rating of each product line?
    avg_rating_product = """
        select product_line, avg(rating) as avg_rating
        from walmart_analysis
        group by product_line 
        order by avg_rating desc;
    """
    spark.sql(avg_rating_product).show()
    logger.info(f'Executed avg_rating_product')

    # --Sales
    # --Number of sales made in each time of the day per weekday
    sales_time_and_day = """
    select 
        day_name,
        time_of_day, 
        count(*) as sales
    from walmart_analysis
    group by day_name, time_of_day
    order by day_name, sales desc;
    """
    spark.sql(sales_time_and_day).show()
    logger.info(f'Executed sales_time_and_day')

    # --Which of the customer types brings the most revenue?
    customers_revenue = """
        select sum(total) total_revenue, customer_type
        from walmart_analysis
        group by customer_type
        order by total_revenue desc;
    """
    spark.sql(customers_revenue).show()
    logger.info(f'Executed customers_revenue')

    # --Which city has the largest tax percent/ VAT (Value Added Tax)?
    city_tax = """
        select city, avg(tax) as avg_tax
        from walmart_analysis
        group by city
        order by avg_tax desc;
    """
    spark.sql(city_tax).show()
    logger.info(f'Executed city_tax')

    # --Which customer type pays the most in VAT?
    customer_vat = """
        select customer_type, sum(tax) as total_tax
        from walmart_analysis
        group by customer_type
        order by total_tax desc;
    """
    spark.sql(customer_vat).show()
    logger.info(f'Executed customer_vat')

    # --Customer
    # --How many unique customer types does the data have?
    unique_customers = """
        select distinct customer_type
        from walmart_analysis;
    """
    spark.sql(unique_customers).show()
    logger.info(f'Executed unique_customers')

    # --How many unique payment methods does the data have?
    unique_payment = """
        select distinct payment
        from walmart_analysis;
    """
    spark.sql(unique_payment).show()
    logger.info(f'Executed unique_payment')

    # --What is the most common customer type?
    common_customer = """
        select customer_type, count(customer_type)
        from walmart_analysis
        group by customer_type
        order by count(customer_type) desc;
    """
    spark.sql(common_customer).show()
    logger.info(f'Executed common_customer')

    # --Which customer type buys the most?
    customers_buy = """
        select customer_type, sum(quantity)
        from walmart_analysis
        group by customer_type
        order by sum(quantity) desc;
    """
    spark.sql(customers_buy).show()
    logger.info(f'Executed customers_buy')

    # --What is the gender of most of the customers?
    gender_customers = """
        select customer_type, gender, count(gender)
        from walmart_analysis
        group by customer_type, gender
        order by count(gender) desc;
    """
    spark.sql(gender_customers).show()

    logger.info(f'Executed gender_customers')

    # --What is the gender distribution per branch?
    genders_branch = """
        select branch, gender, count(gender)
        from walmart_analysis
        group by branch, gender
        order by branch, count(gender) desc; 
    """
    spark.sql(genders_branch).show()
    logger.info(f'Executed genders_branch')

    # --Which time of the day do customers give most ratings?
    time_most_ratings = """
        select time_of_day, avg(rating)
        from walmart_analysis
        group by time_of_day
        order by avg(rating) desc;
    """
    spark.sql(time_most_ratings).show()
    logger.info(f'Executed time_most_ratings')

    # --Which time of the day do customers give most ratings per branch?
    time_best_avg_ratings = """
        select branch, time_of_day, avg(rating)
        from walmart_analysis
        group by time_of_day, branch
        order by branch, avg(rating) desc;
    """
    spark.sql(time_best_avg_ratings).show()
    logger.info(f'Executed time_best_avg_ratings')

    # --Which day fo the week has the best avg ratings?
    day_best_avg_ratings = """
        select day_name, avg(rating)
        from walmart_analysis
        group by day_name
        order by avg(rating) desc;
    """
    spark.sql(day_best_avg_ratings).show()
    logger.info(f'Executed day_best_avg_ratings')

    # Which day of the week has the best average ratings per branch?
    best_average_ratings_per_branch = """
        select branch, day_name, avg(rating)
        from walmart_analysis
        group by day_name, branch
        order by branch, avg(rating) desc;
    """
    spark.sql(best_average_ratings_per_branch).show()

    logger.info(f'Executed best_average_ratings_per_branch')
    logger.info(f'Executed complete.')
