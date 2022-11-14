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
        config = {"spark.kubernetes.container.image": "hareendranvr/executor:latest","spark.kubernetes.container.image.pullPolicy": "Never",
                "spark.executor.instances": 2,
                "spark.kubernetes.executor.request.cores": 2,}
        spark = self.get_spark_session("jy-spark-executor", SparkConf(config),config=config)
        print(spark)
        return spark

'''
set DATABRICKS_ADDRESS=https://adb-40310182645720.0.azuredatabricks.net
set DATABRICKS_API_TOKEN=dapi92bd68eed4d4d371efb2ab70d617f672
set DATABRICKS_CLUSTER_ID=0523-064935-ruesezri
set DATABRICKS_ORG_ID=40310182645720
set DATABRICKS_PORT=15001
'''

os.environ["DATABRICKS_ADDRESS"] = "https://adb-40310182645720.0.azuredatabricks.net"
os.environ["DATABRICKS_API_TOKEN"] = "dapi92bd68eed4d4d371efb2ab70d617f672"
os.environ["DATABRICKS_CLUSTER_ID"] = "0523-064935-ruesezri"
os.environ["DATABRICKS_ORG_ID"] = "40310182645720"
os.environ["DATABRICKS_PORT"] = "15001"
# os.environ["PYSPARK_PYTHON"] = "python3"
# os.environ["SPARK_HOME"] = r"venv/lib/site-packages/pyspark"

# spark = SparkSession.\
#         builder.\
#         appName("pyspark").\
#         master("k8s://https://kubernetes.docker.internal:6443").\
#         config("spark.executor.memory", "512m").\
#         getOrCreate()
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


