from pyspark.sql import SparkSession

from walmart_analysis.settings import HOST, DB_NAME, PASSWORD, USER

spark = (
    SparkSession.builder.
    appName("PostgreSQL Connection").
    config("spark.jars", "postgresql-42.7.10.jar").
    getOrCreate()
)

url = f"jdbc:postgresql://{HOST}:5432/{DB_NAME}"

properties = {
    "user": USER,
    "password": PASSWORD,
    "driver": "org.postgresql.Driver"
}

table_name = "walmart_sales"

df = spark.read.jdbc(url, table_name, properties=properties)

df.createOrReplaceTempView("walmart_analysis")
# df.show(df.count(), truncate=False)

# How many unique cities does the data have?
unique_cities = """
    select count(distinct City) as unique_cities
    from walmart_analysis;
"""

spark.sql(unique_cities).show()

# In which city is each branch?
branch_city = """
    select distinct Branch, City
    from walmart_analysis;
"""
spark.sql(branch_city).show()

# How many unique product lines does the data have?
unique_product_lines = """
    select distinct Product_line
    from walmart_analysis;
"""
spark.sql(unique_product_lines).show()

# What is the most common payment method?
common_payment_method = """
    select Payment, count(Payment) as count
    from walmart_sales
    group by Payment
    order by count DESC
    limit 1;
"""
spark.sql(common_payment_method).show()

# What is the most selling product line?

# print(result_df)
