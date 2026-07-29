import sys
import os
from pyspark.sql.functions import *
from lib import data_reader, utils, data_manipulation
from logger import Log4j

#adding feature1 to test git pull request
#adding featur1 in main

if __name__=="__main__":
    if len(sys.argv)<2:
        print(sys.argv)
        print("specify the environment")
        sys.exit(-1)

    job_run_env = sys.argv[1]

    # Ensure local runs do not inherit conflicting global Spark env vars
    utils.remove_global_spark_env_vars()

    spark = utils.create_spark_session(job_run_env)
    logger =Log4j(spark)
    logger.info("Spark Session created successfully")


    customers_df = data_reader.read_customers(spark,job_run_env)
    orders_df = data_reader.read_orders(spark,job_run_env)

    # Get closed orders
    closed_orders_df = data_manipulation.get_closed_orders(orders_df)

    # Join customers and orders
    joined_df = data_manipulation.join_customers_orders(closed_orders_df, customers_df)

    grouped_df = data_manipulation.get_statewise_order_count(joined_df)

    logger.info("---------------- Closed Orders ----------------")
    closed_orders_df.show(10)

    logger.info("---------------- Joined Data ----------------")
    joined_df.show(10)

    logger.info("---------------- Statewise Order Count ----------------")
    grouped_df.show(10)

    # Stop Spark gracefully
    spark.stop()

    logger.info("Spark session stopped successfully.")
    
