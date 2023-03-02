from etcd3 import Etcd3Client


class EtcdRegistry:
    def __init__(self, etcd_host: str, etcd_port: int):
        self.etcd_client = Etcd3Client(host=etcd_host, port=etcd_port)

    def register_service(self, service_name: str, service_address: str, service_port: int):
        service_key = f"/services/{service_name}"
        service_value = f"{service_address}:{service_port}"
        self.etcd_client.put(service_key, service_value)

    def get_service_endpoint(self, service_name: str) -> str:
        service_key = f"/services/{service_name}"
        result = self.etcd_client.get(service_key)
        if result.count == 0:
            return None
        return result.kvs[0].value

