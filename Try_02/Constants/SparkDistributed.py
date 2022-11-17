import os
class SparkDistributed:
    executor_pod_image = os.environ.get("executor_pod_image")
    executor_request_cpu =  os.environ.get("executor_request_cpu")
    executor_request_memory = os.environ.get("executor_request_memory")
    executor_limit_cpu = os.environ.get("executor_limit_cpu")
    executor_limit_memory = os.environ.get("executor_limit_memory")
    number_of_executors = os.environ.get("number_of_executors")
    service_account = os.environ.get("service_account")
    driver_service_name = os.environ.get("driver_service_name")
    namespace = os.environ.get("namespace")
