import os
class SparkDistributed:
    executor_pod_image = "hareendranvr/execute"
    executor_request_cpu =  "2"
    executor_request_memory = "1g"
    executor_limit_cpu = "4"
    executor_limit_memory = "8g"
    number_of_executors = "2"
    service_account = "default"
    driver_service_name = "sk8r"
    namespace = "default"
