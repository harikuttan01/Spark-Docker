import requests
class Volumes:
    def volume_custom_mount(project_id=None, minio_bucket=None, resource_quota_full=None):
        volume = []
        desc = {
            "name": project_id,
            "mountPath": "/data",
            "subPath": f"{minio_bucket}/{project_id}/{project_id}-Data"
        }
        if resource_quota_full:
            desc["readOnly"]=True
        volume.append(desc)
        return volume

    def volume_mount_count(project_id, username):
        url = f"http://mosaic-console-backend/mosaic-console-backend/secured/api/pvc/project/{project_id}"
        url2 = f"http://mosaic-console-backend/mosaic-console-backend/secured/api/pvc/project/all"    
        volume = []
        headers = {"X-Auth-Username": username}
        for item in [url, url2]:
            response = requests.get(item, headers=headers)
            response = response.json()
            if response:
                for x in range(len(response)):
                    desc = {
                        "name": response[x]["pvcName"],
                        "mountPath": response[x]["mountpath"],
                    }
                    volume.append(desc)
        return volume