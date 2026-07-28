from lib import config_reader
#creating customers schema
def get_customers_schema():
    schema = """customer_id INT, customer_fname STRING, customer_lname STRING, customer_email STRING, customer_password STRING, customer_street STRING,
    customer_city STRING,
    customer_state STRING,
    customer_zipcode STRING
    """
    return schema

def read_customers(spark,env):
    config = config_reader.get_app_conf(env)
    customers_file_path = config["customers.file.path"]
    return spark.read \
            .format("csv") \
            .option("header",True) \
            .schema(get_customers_schema()) \
            .load(customers_file_path)

#creating orders schema
def get_orders_schema():
    schema = """order_id INT,order_date STRING,order_customer_id INT,order_status STRING"""
    return schema

def read_orders(spark,env):
    config=config_reader.get_app_conf(env)
    orders_file_path = config["orders.file.path"]
    return spark.read \
            .format("csv") \
            .schema(get_orders_schema()) \
            .option("header",False) \
            .load(orders_file_path)