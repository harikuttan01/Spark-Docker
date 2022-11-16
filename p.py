from mystiko import k8s
k8s_secrets = k8s.get_secrets()
db_pwd = k8s_secrets['DB_PASSWORD']
print(db_pwd)