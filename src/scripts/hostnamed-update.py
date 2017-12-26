import os
import yaml
import click
import hashlib
import requests
from zencore.utils.system import get_main_ipaddress


@click.group()
def hostnamed():
    pass


@hostnamed.command()
@click.option("-c", "--config", default="~/.hostnamed.conf")
def config(config):
    """Make settings."""
    config = os.path.expanduser(config)
    server = ""
    hostname = ""
    update_key = ""
    use_local_ip = ""
    while not server:
        server = input("Server Address: ")
    while not hostname:
        hostname = input("Hostname: ")
    while not update_key:
        update_key = input("Key: ")
    while not use_local_ip in ("y", "n"):
        use_local_ip = input("Use local IP (y/n): ").lower()
    if use_local_ip == "y":
        use_local_ip = True
    else:
        use_local_ip = False
    settings = {
        "server": server,
        "hostname": hostname,
        "update_key": update_key,
        "use_local_ip": use_local_ip,
    }
    str_settings = yaml.dump(settings)
    with open(config, "w", encoding="utf-8") as fobj:
        fobj.write(str_settings)


@hostnamed.command()
@click.option("-c", "--config", default="~/.hostnamed.conf")
def update(config):
    """Do update."""
    config = os.path.expanduser(config)
    if not os.path.exists(config):
        print("Provide settings before update! --help see more information.")
        os.sys.exit(1)
    with open(config, "r", encoding="utf-8") as fobj:
        str_settings = fobj.read()
    try:
        settings = yaml.load(str_settings)
    except Exception as error:
        print("Parse config file failed.")
        os.sys.exit(2)
    if (not "server" in settings) and (not "hostname" in settings) and (not "update_key" in settings) and (not "use_loca_ip" in settings):
        print("Bad config file missing required fields.")
        os.sys.exit(3)
    ip = ""
    if settings["use_local_ip"]:
        ip = get_main_ipaddress()
    text = "hostname={hostname}&ip={ip}&key={update_key}".format(ip=ip, **settings)
    code = hashlib.md5(text.encode("utf-8")).hexdigest()
    data = {
        "hostname": settings["hostname"],
        "ip": ip,
        "code": code,
    }
    response = requests.get(settings["server"], params=data)
    if response.status_code == 200:
        print("OK")
    else:
        print("ERROR")


if __name__ == "__main__":
    hostnamed()
