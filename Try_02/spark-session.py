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
            "spark.kubernetes.container.image.pullSecrets": "canvas-secret",
            "spark.kubernetes.container.image.pullPolicy": "Always",
            "spark.executor.instances": SparkDistributed.number_of_executors,
            "spark.kubernetes.executor.request.cores": SparkDistributed.executor_request_cpu,
            "spark.executor.cores": SparkDistributed.executor_request_cpu,
            "spark.executor.memory": SparkDistributed.executor_request_memory,
            "spark.kubernetes.authenticate.driver.serviceAccountName":SparkDistributed.service_account,
            # At least 500m memory is required.
            "spark.driver.blockManager.port": "7777",
            "spark.driver.port": "2222",
            "spark.driver.host": str(SparkDistributed.driver_service_name) + "." + str(SparkDistributed.namespace)
                                + ".svc.cluster.local",  # service-name.namespace.svc.cluster.local
            "spark.driver.bindAddress": "0.0.0.0",
            # "spark.jars": "/opt/conda/lib/python3.7/site-packages/pyspark/jars"
            # https://spark.apache.org/docs/2.4.3/running-on-kubernetes.html -> Configuration
        }

    def get_spark_session(self,app_name: str, conf: SparkConf,config):
        print("Launching Spark Session! ...\n")
        conf = conf.setMaster("k8s://https://kubernetes.default.svc.cluster.local")
        print("Spark master is running on k8....\n")

        for key, value in config.items():
            conf.set(key, value)
        session = SparkSession.builder.appName(app_name).config(conf=conf).getOrCreate()
        return session


#k8s://https://kubernetes.default.svc.cluster.local
#k8s://https://kubernetes.docker.internal:6443

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
spark.sql('DROP TABLE IF EXISTS demo_temps_table')
temps.write.saveAsTable('demo_temps_table')
spark.sql("SHOW DATABASES").show()
spark.sql("SHOW TABLES").show()
df_temps = spark.sql("SELECT AirportCode,TempHighF FROM demo_temps_table " \
    "WHERE AirportCode != 'BLI' AND Date > '2021-04-01' " \
    "GROUP BY AirportCode, Date, TempHighF, TempLowF " \
    "ORDER BY TempHighF DESC")

print("df:",df_temps)
df_temps.show()

# # spark.sql('DROP TABLE demo_temps_table')


