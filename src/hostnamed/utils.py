import time
import hashlib
import requests


def get_update_code(hostname, ip, key):
    text = "hostname={}&ip={}&key={}".format(hostname, ip, key)
    return hashlib.md5(text.encode("utf-8")).hexdigest()

def get_query_code(hostname, timestamp, key):
    text = "hostname={}&timestamp={}&key={}".format(hostname, timestamp, key)
    return hashlib.md5(text.encode("utf-8")).hexdigest()

def client_update(server, hostname, key, ip=""):
    params = {
        "hostname": hostname,
        "ip": ip,
        "code": get_update_code(hostname, ip, key),
    }
    response = requests.get(server, params=params)
    if response.status_code == 200:
        return True
    return False


def client_query(server, hostname, key):
    timestamp = int(time.time())
    params = {
        "hostname": hostname,
        "timestamp": timestamp,
        "code": get_query_code(hostname, timestamp, key),
    }
    response = requests.get(server, params=params)
    if response.status_code == 200:
        return response.text
    return "ERROR"
