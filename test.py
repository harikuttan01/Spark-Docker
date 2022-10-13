from pyspark.sql import SparkSession

myspark = SparkSession.\
        builder.\
        appName("pyspark").\
        master("spark://192.168.1.106:7077").\
        config("spark.executor.memory", "512m").\
        getOrCreate()

myspark.read.csv('iris.data')