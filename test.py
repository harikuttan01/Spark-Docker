from pyspark.sql import SparkSession

myspark = SparkSession.\
        builder.\
        appName("pyspark").\
        master("spark://127.0.0.1:7077").\
        config("spark.executor.memory", "512m").\
        getOrCreate()

# myspark.read.csv('iris.data')
print(myspark)