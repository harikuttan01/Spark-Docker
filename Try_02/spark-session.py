from pyspark import SparkConf
import re
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from datetime import date
import os
import wget
from Constants.SparkDistributed import SparkDistributed

class Sk8r:
    def get_configs(self):

        return {
            "spark.kubernetes.namespace": SparkDistributed.namespace,
            "spark.kubernetes.container.image": SparkDistributed.executor_pod_image,
            "spark.kubernetes.container.image.pullSecrets": "regcred",
            "spark.kubernetes.container.image.pullPolicy": "IfNotPresent",
            "spark.executor.instances": SparkDistributed.number_of_executors,
            "spark.kubernetes.executor.request.cores": SparkDistributed.executor_request_cpu,
            "spark.executor.cores": SparkDistributed.executor_request_cpu,
            "spark.executor.memory": SparkDistributed.executor_request_memory,
            "spark.kubernetes.authenticate.driver.serviceAccountName":SparkDistributed.service_account,
            # At least 500m memory is required.
            "spark.driver.blockManager.port": "7777",
            "spark.driver.port": "2222",
            "spark.driver.host": str(SparkDistributed.driver_service_name) + "." + str(SparkDistributed.namespace)
                                + ".svc.cluster.local", 
            "spark.driver.bindAddress": "0.0.0.0",

        }

    def get_spark_session(self,app_name: str, conf: SparkConf,config):
        print("Launching Spark Session! ...\n")
        conf = conf.setMaster("k8s://https://kubernetes.default.svc.cluster.local")
        print("Spark master is running on k8....\n")

        for key, value in config.items():
            conf.set(key, value)
        session = SparkSession.builder.appName(app_name).config(conf=conf).getOrCreate()
        return session



s = Sk8r()
config = s.get_configs()
spark = s.get_spark_session("executor",SparkConf(config),config=config)

schema = StructType([
    StructField('AirportCode', StringType(), False),
    StructField('Date', DateType(), False),
    StructField('TempHighF', IntegerType(), False),
    StructField('TempLowF', IntegerType(), False)
])


print(schema)
data = [
    [ 'BLI', date(2021, 4, 3), 52, 43],
    [ 'BLI', date(2021, 4, 2), 50, 38],
    [ 'BLI', date(2021, 4, 1), 52, 41],
    [ 'PDX', date(2021, 4, 3), 64, 45],
    [ 'PDX', date(2021, 4, 2), 61, 41],
    [ 'PDX', date(2021, 4, 1), 66, 39],
    [ 'SEA', date(2021, 4, 3), 57, 43],
    [ 'SEA', date(2021, 4, 2), 54, 39],
    [ 'SEA', date(2021, 4, 1), 56, 41]
]

temps = spark.createDataFrame(data, schema)
temps.show()

spark.sql('USE default')
temps.createOrReplaceTempView("temp_view")

spark.sql("SHOW DATABASES").show()

df_temps = spark.sql("SELECT * FROM temp_view " \
    "WHERE AirportCode != 'BLI' AND Date > '2021-04-01' " \
    "GROUP BY AirportCode, Date, TempHighF, TempLowF " \
    "ORDER BY TempHighF DESC")

spark.sql("SELECT COUNT(*) FROM temp_view ;").show()
print("df:",df_temps)
df_temps.show()

print("--------------------------------------------------------------------------------------------------------------------------------------------------")

print("Reading from files.....\n")
dataframe = spark.read.json('nyt2.json')

dataframe.show()

print("Dropping duplicates.....\n")
dataframe_dropdup = dataframe.dropDuplicates() 
dataframe_dropdup.show(10)

print("Selecting specific columns without sql.....\n")
dataframe.select("author", "title", "rank", "price").show(10)

print("Matching entries using values.....\n")
dataframe [dataframe.author.isin("John Sandford", 
"Emily Giffin")].show(5)

print("Matching entries with expressions.....\n")
dataframe.select("author", "title",dataframe.title.like("% THE %")).show(15)

print("Groupby function.....\n")
dataframe.groupBy("author").count().show(10)

print("Using filters.....\n")
dataframe.filter(dataframe["title"] == 'THE HOST').show(5)

print("Creating partitions.....\n")
dataframe.repartition(10).rdd.getNumPartitions()

print("Performing SQL queries.....\n")
dataframe.createOrReplaceTempView("df")
spark.sql("select * from df").show(3)
try:
    dft = spark.sql("select " \
        "CASE WHEN description LIKE '%love%' THEN 'Love_Theme' " \
            "WHEN description LIKE '%hate%' THEN 'Hate_Theme' " \
                "WHEN description LIKE '%happy%' THEN 'Happiness_Theme' " \
                    "WHEN description LIKE '%anger%' THEN 'Anger_Theme' " \
                        "WHEN description LIKE '%horror%' THEN 'Horror_Theme' " \
                            "WHEN description LIKE '%death%' THEN 'Criminal_Theme' " \
                                "WHEN description LIKE '%detective%' THEN 'Mystery_Theme' " \
                                    "ELSE 'Other_Themes' " \
                                        "END Themes " \
                                            "from df ")
    dft.groupBy('Themes').count().show()
except:
    pass


