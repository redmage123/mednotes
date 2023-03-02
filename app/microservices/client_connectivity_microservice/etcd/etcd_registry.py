import etcd3

class EtcdRegistry:
    def __init__(self, host, port):
        self.client = etcd3.client(host=host, port=port)

    def register_service(self, service_name, service_host, service_port):
        endpoint = "{}:{}".format(service_host, service_port)
        self.client.put('/services/{}'.format(service_name), endpoint)

    def get_service_endpoint(self, service_name):
        result = self.client.get('/services/{}'.format(service_name))
        if result is None:
            return None
        return result[0].decode('utf-8')

