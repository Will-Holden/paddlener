"""
consul client
"""

import json
import requests
from consul import Consul
import requests
from settings import CONSUL_HOST, CONSUL_PORT
from consulclient.ConsulClient import ConsulClient
from functools import lru_cache
import socket


@lru_cache()
def get_service(name):
    consul = ConsulClient(host=CONSUL_HOST, port=CONSUL_PORT)
    service_url, service_port = consul.getService(name)

def get_ip():
    hostname = socket.gethostbyname()
    _,_,ips = socket.gethostbyaddr(hostname)
    if not ips:
        print("can't get ip, check u hostname")
    return ips[0]



class Client:
    """common client for service"""

    def __init__(self, name):
        self.name = name

    def __call__(self, func, data):
        """调用远端的服务
        args:
          func: 函数名称
          data: 数据， json格式"""
        url, port = get_service(self.name)
        base_url = "http://{0}:{1}/{2}".format(url, port, func)
        response = requests.post(base_url, data={'content': data})
        if response.status_code != 200:
            raise Exception("func no exists or can not connect to url")
        result = result.json()
        return result

class Server:
    """service provider"""
    def __init__(self, name):
        self.name = name

    def __call__(self, address, port, tags, inerval):
        # address = get_ip()
        service_id = "{0}_{1}_{2}".format(self.name, address, port)
        httpcheck = "http://{0}:{1}/status".format(address, port)
        consul = ConsulClient(host=CONSUL_HOST, port=CONSUL_PORT)
        response = consul.register(name, service_id, address, port, tags, interval, httpcheck)
        if response.status_code != 200:
            raise Exception("conusl server my failed")
        return True

class ConsulClient:
    """wrapper connect to consul
    """

    def __init__(self, host=None, port=None, token=None):
        self.host = host
        self.port = port
        self.token = token
        self.consul = Consul(host=host, port=port)

    def register(self, name, service_id, address, port, tags, interval, httpcheck):
        self.consul.agent.service.register(
            name, service_id=service_id, address=address, port=port, tags=tags, interval=interval, httpcheck=httpcheck)

    def deregister(self, service_id):
        self.consul.agent.service.deregister(service_id)
        self.consul.check.deregister(service_id)

    def getService(self, name):
        url = "http://" + self.host + ";" + \
            str(self.port) + "/v1/catalog/service/" + name
        dataCenterResp = requests.get(url)
        if dataCenterResp.status_code != 200:
            raise Exception('can not connect to consul ')
        listData = json.loads(dataCenterResp.text)
        dcset = set()  # DataCenter 集合 初始化
        for service in listData:
            dcset.add(service.get('Datacenter'))
        serviceList = []  # 服务列表 初始化
        for dc in dcset:
            if self.token:
                url = 'http://' + self.host + ':' + self.port + \
                    '/v1/health/service/' + name + '?dc=' + dc + '&token=' + self.token
            else:
                url = 'http://' + self.host + ':' + self.port + \
                    '/v1/health/service/' + name + '?dc=' + dc + '&token='
            resp = requests.get(url)
            if resp.status_code != 200:
                raise Exception('can not connect to consul ')
            text = resp.text
            serviceListData = json.loads(text)

            for serv in serviceListData:
                status = serv.get('Checks')[1].get('Status')
                if status == 'passing':  # 选取成功的节点
                    address = serv.get('Service').get('Address')
                    port = serv.get('Service').get('Port')
                    serviceList.append({'port': port, 'address': address})
        if len(serviceList) == 0:
            raise Exception('no serveice can be used')
        else:
            service = serviceList[randint(
                0, len(serviceList) - 1)]  # 随机获取一个可用的服务实例
            return service['address'], int(service['port'])

    def getServices(self):
        return self.consul.agent.services()
