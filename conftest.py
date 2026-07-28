import pytest
from lib.utils import create_spark_session

@pytest.fixture
def spark():
    """Fixture to create a Spark session for testing purposes."""
    spark = create_spark_session("LOCAL")
    yield spark
    spark.stop()

@pytest.fixture
def customers(spark):
    """Fixture to create a DataFrame for customers."""
    customers_schema = "customer_state string,count int"
    return spark.read \
        .format("csv") \
        .option("header", True) \
        .schema(customers_schema) \
        .load("data/test_result/state_aggregate.csv")
