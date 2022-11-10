from pyspark.sql import SparkSession
from pyspark.sql.types import *
from datetime import date
import os
import subprocess

subprocess.call(['bin/spark-class', 'org.apache.spark.deploy.master.Master', '>>', 'logs/spark-master.out'], shell=True)
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

spark = SparkSession.\
        builder.\
        appName("pyspark").\
        master("local[*]").\
        config("spark.executor.memory", "512m").\
        getOrCreate()

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




#f"spark://{os.environ.get('SPARK_MASTER_HOST')}:7077"