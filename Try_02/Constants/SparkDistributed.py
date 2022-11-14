import os
class SparkDistributed:
    executor_pod_image = "spark:latest"
    executor_request_cpu =  "2"
    executor_request_memory = "2000M"
    executor_limit_cpu = "2"
    executor_limit_memory = "2000M"
    number_of_executors = "2"
    service_account = "default"
    # executor_service_name = os.getenv("pod_name") 
    # pvc_name = os.getenv("pvc_name")
    # project_id = os.getenv("PROJECT_ID")
    # user_id = os.getenv("userId")
    # minio_data_bucket = os.getenv("MINIO_DATA_BUCKET")
    # namespace = os.getenv("NAMESPACE")
    # is_job_run = os.getenv("is_job_run")
    # PYTHONPATH = os.getenv("PYTHONPATH")