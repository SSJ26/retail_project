from pyspark.sql import SparkSession
from lib.config_reader import get_pyspark_conf

def create_spark_session(env):
    if env == "LOCAL":
        return SparkSession.builder \
                .config(conf=get_pyspark_conf(env)) \
                .config("spark.driver.extraJavaOptions", "-Dlog4j.configuration=file:log4j.properties") \
                .master("local[2]") \
                .getOrCreate()
    else:
        return SparkSession.builder \
                .config(conf=get_pyspark_conf(env)) \
                .enableHiveSupport() \
                .getOrCreate()

def remove_global_spark_env_vars():
    """Ensure local runs do not inherit conflicting global Spark env vars"""
    import os
    os.environ.pop("SPARK_HOME", None)
    os.environ.pop("PYSPARK_PYTHON", None)
    os.environ.pop("PYSPARK_DRIVER_PYTHON", None)
    print("Cleared SPARK_HOME, PYSPARK_PYTHON, PYSPARK_DRIVER_PYTHON for LOCAL run")