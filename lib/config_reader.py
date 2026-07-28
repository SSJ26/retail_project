import configparser
from pyspark import SparkConf

def get_app_conf(env):
    """fetching application configaration details"""
    config = configparser.ConfigParser()
    config.read("config/application.conf")
    app_conf = {}

    for (key,value) in config.items(env):
        #print(key,value)
        app_conf[key]=value

    return app_conf

def get_pyspark_conf(env):
    """ fetching pyspark configurations details """
    config = configparser.ConfigParser()
    config.read("config/pyspark.conf")
    pyspark_conf = SparkConf()

    for key,value in config.items(env):
        pyspark_conf.set(key,value)    
    
    return pyspark_conf