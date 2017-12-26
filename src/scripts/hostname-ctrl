#!/usr/bin/env python
import os
import urllib
import yaml
import click
import hashlib
import requests
from hostnamed.utils import load_config
from hostnamed.utils import input_config
from hostnamed.utils import save_config
from hostnamed.utils import client_update


@click.group()
def hostnamed():
    pass


@hostnamed.command()
@click.option("-c", "--config", default="~/.hostnamed.conf")
def config(config):
    """Make settings."""
    settings = load_config(config)
    new_entry = input_config()
    settings.update(new_entry)
    save_config(settings, config)


@hostnamed.command()
@click.option("-c", "--config", default="~/.hostnamed.conf")
@click.argument("hostnames", nargs=-1)
def update(config, hostnames):
    """Do update."""
    settings = load_config(config)
    if not hostnames:
        hostnames = list(settings.keys())
    for hostname in hostnames:
        config = settings[hostname]
        update_url = urllib.parse.urljoin(config["server"], "update/")
        result = client_update(update_url, hostname, config["update-key"], config["use-local-ip"])
        if result:
            print("{} OK".format(hostname))
        else:
            print("{} FAILED".format(hostname))


if __name__ == "__main__":
    hostnamed()
