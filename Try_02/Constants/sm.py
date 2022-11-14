from pyspark import SparkConf
from pyspark.sql import SparkSession
import re
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
        config = {"spark.kubernetes.container.image": "spark:latest","spark.kubernetes.container.image.pullPolicy": "Never",
                "spark.executor.instances": 2,
                "spark.kubernetes.executor.request.cores": 2,}
        spark = self.get_spark_session("jy-spark-executor", SparkConf(config),config=config)
        return spark


