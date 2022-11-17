from pyspark import SparkConf
from pyspark.sql import SparkSession
import re
from pyspark.sql.types import *
from datetime import date
import os

class SSession:
    def get_spark_session(self,app_name: str, conf: SparkConf,config):
        print("Launching Spark Session! ...\n")
        conf = conf.setMaster("k8s://https://kubernetes.docker.internal:6443")
        print("this is the k8 master")
        # session = SparkSession.builder.appName(app_name).config(conf=conf).getOrCreate()
        for key, value in config.items():
            conf.set(key, value)
        session = SparkSession.builder.appName(app_name).config(conf=conf).getOrCreate()
        return session
    def session_creator(self):
        config = {"spark.kubernetes.container.image": "hareendranvr/executor","spark.kubernetes.container.image.pullPolicy": "Always",
                "spark.executor.instances": 2,"spark.kubernetes.container.image.pullSecrets": "regcred",
                "spark.kubernetes.executor.request.cores": 2,"spark.driver.blockManager.port": "7777", "spark.driver.host": str(SparkDistributed.executor_service_name) + "." + str(SparkDistributed.namespace)+ ".svc.cluster.local",
        "spark.driver.port": "2222",
        "spark.driver.bindAddress": "0.0.0.0",}
        spark = self.get_spark_session("jy-spark-executor", SparkConf(config),config=config)
        print(spark)
        return spark

s = SSession()
spark = s.session_creator()

schema = StructType([
    StructField('AirportCode', StringType(), False),
    StructField('Date', DateType(), False),
    StructField('TempHighF', IntegerType(), False),
    StructField('TempLowF', IntegerType(), False)
])

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

spark.sql('USE default')
spark.sql('DROP TABLE IF EXISTS demo_temps_table')
temps.write.saveAsTable('demo_temps_table')

df_temps = spark.sql("SELECT * FROM demo_temps_table " \
    "WHERE AirportCode != 'BLI' AND Date > '2021-04-01' " \
    "GROUP BY AirportCode, Date, TempHighF, TempLowF " \
    "ORDER BY TempHighF DESC")
df_temps.show()

spark.sql('DROP TABLE demo_temps_table')


