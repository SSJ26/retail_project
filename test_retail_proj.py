import pytest
from lib.data_reader import read_customers, read_orders
from lib.utils import create_spark_session, remove_global_spark_env_vars
from lib.config_reader import get_pyspark_conf, get_app_conf
from lib.data_manipulation import get_closed_orders, get_statewise_order_count, get_generic_order_status_count
from pyspark.sql.functions import count

# Ensure local runs do not inherit conflicting global Spark env vars
remove_global_spark_env_vars()

@pytest.mark.skip()
def test_read_customers(spark):
    customers_df = read_customers(spark, "LOCAL")
    customers_count = customers_df.count()
    print(f"Number of customers read from the file: {customers_count}")
    assert customers_count == 20

@pytest.mark.skip()
def test_read_orders(spark):
    orders_count = read_orders(spark, "LOCAL").count()
    print(f"Number of orders read from the file: {orders_count}")
    assert orders_count == 25831125

@pytest.mark.skip()
#@pytest.mark.transformation
def test_get_closed_orders(spark):
    orders_df = read_orders(spark, "LOCAL")
    closed_orders_count = get_closed_orders(orders_df).count()
    print(f"Number of closed orders: {closed_orders_count}")
    assert closed_orders_count == 2833500  # Replace 1000 with the expected count

@pytest.mark.skip(reason="Skipping this test as it requires a specific environment setup.")
def test_get_app_conf():
    config = get_app_conf("LOCAL")
    assert "customers.file.path" in config

@pytest.mark.skip()
#@pytest.mark.transformation
def test_get_statewise_order_count(spark,customers):
    customers_df = read_customers(spark, "LOCAL")
    order_count_df = get_statewise_order_count(customers_df)
    assert sorted(order_count_df.collect()) == sorted(customers.collect())

@pytest.mark.parametrize(
    "status,expected_count",
    [
        ("CLOSED", 2833500),
        ("COMPLETE",8587125)
    ]
)
def test_get_generic_order_status_count(spark,status,expected_count):
    orders_df = read_orders(spark, "LOCAL")
    count = get_generic_order_status_count(orders_df, status)
    print(f"Number of orders with status '{status}': {count}")
    assert expected_count == count