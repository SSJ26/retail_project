from pyspark.sql.functions import *

def get_closed_orders(orders_df):
    """returns only closed orders from the orders dataframe"""
    closed_orders = orders_df.filter(orders_df.order_status == "CLOSED")
    return closed_orders

def join_customers_orders(orders_df, customers_df):
    """joins customers and orders dataframes on customer_id"""
    return orders_df.join(broadcast(customers_df), customers_df.customer_id == orders_df.order_customer_id, "inner")

def get_statewise_order_count(joined_df):
    """returns the count of orders per state"""
    return joined_df.groupBy("customer_state").agg(count("*").alias("count")).sort("count", ascending=False)

def get_generic_order_status_count(orders_df, status):
    """returns the count of orders for a specific order_status"""
    return orders_df.filter(orders_df.order_status == status).count()