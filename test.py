from pyspark.sql import SparkSession

myspark = SparkSession.\
        builder.\
        appName("pyspark").\
        master("local[*]").\
        config("spark.executor.memory", "512m").\
        getOrCreate()

# myspark.read.csv('iris.data')
print(myspark)