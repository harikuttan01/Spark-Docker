from pyspark import SparkConf
import re
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from datetime import date
import os
from Constants.SparkDistributed import SparkDistributed
# from Volumes.Volumes import Volumes


def get_memory(memory):
    try:
        temp = re.compile("([0-9\.]+)([a-zA-Z]+)")
        res = temp.match(memory).groups()
        if 'M' in res[1]:
            if float(res[0]) >= 500:
                return str(res[0]) + "m"
            else:
                return "500m"
        elif 'G' in res[1]:
            return str(res[0]) + "g"
    except Exception as ex:
        print(f"Memory issue: {ex}")
        return None


def get_configs():

    return {
        "spark.kubernetes.namespace": SparkDistributed.namespace,
        "spark.kubernetes.container.image": SparkDistributed.executor_pod_image,
        "spark.kubernetes.container.image.pullSecrets": "regcred",
        "spark.kubernetes.container.image.pullPolicy": "Always",
        "spark.executor.instances": SparkDistributed.number_of_executors,
        "spark.kubernetes.executor.request.cores": SparkDistributed.executor_request_cpu,
        "spark.kubernetes.executor.limit.cores": SparkDistributed.executor_limit_cpu,
        "spark.executor.cores": SparkDistributed.executor_request_cpu,
        "spark.executor.memory": get_memory(SparkDistributed.executor_limit_memory),
        "spark.kubernetes.authenticate.driver.serviceAccountName":SparkDistributed.service_account,
        # At least 500m memory is required.
        "spark.driver.blockManager.port": "7777",
        "spark.driver.port": "2222",
        "spark.driver.host": str(SparkDistributed.executor_service_name) + "." + str(SparkDistributed.namespace)
                             + ".svc.cluster.local",  # service-name.namespace.svc.cluster.local
        "spark.driver.bindAddress": "0.0.0.0",
        # "spark.jars": "/opt/conda/lib/python3.7/site-packages/pyspark/jars"
        # https://spark.apache.org/docs/2.4.3/running-on-kubernetes.html -> Configuration
    }


def get_spark_session(app_name: str, conf: SparkConf):
    print("Launching Spark Session! ...\n")
    conf = conf.setMaster("k8s://https://kubernetes.default.svc.cluster.local")
    print("Spark master is running on k8....\n")

    for key, value in config.items():
        conf.set(key, value)
    session = SparkSession.builder.appName(app_name).config(conf=conf).getOrCreate()
    return session

config = get_configs()
spark = get_spark_session("jy-spark-executor", SparkConf(config))
print(spark)
# if SparkDistributed.is_job_run:
#     print("Launching Spark Session for JOB RUN!\n")
#     config = {}
#     spark = SparkSession.builder.appName("spark-operator-run").getOrCreate()
# else:
#     # config = add_volume_mounts(get_configs())
#     # config = add_executor_env_variables(config)
#     config = get_configs()
#     spark = get_spark_session("jy-spark-executor", SparkConf(config))

#k8s://https://kubernetes.default.svc.cluster.local
#k8s://https://kubernetes.docker.internal:6443

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
#         master("k8s://https://kubernetes.default.svc.cluster.local").\
#         config("spark.executor.memory", "512m").\
#         getOrCreate()

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
