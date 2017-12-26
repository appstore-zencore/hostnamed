import hashlib
from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.timezone import now
from zencore.django.request import get_client_ip
from .models import Host


def update(request):
    hostname = request.GET.get("hostname")
    ip = request.GET.get("ip", "")
    code = request.GET.get("code")
    client_ip = get_client_ip(request)

    if (not hostname) and (not code):
        raise Http404()

    try:
        host = Host.objects.get(hostname=hostname)
    except Host.DoesNotExist:
        raise Http404()

    raw = "hostname={}&ip={}&key={}".format(host.hostname, ip, host.update_key)
    real_code = hashlib.md5(raw.encode("utf-8")).hexdigest()
    if code != real_code:
        raise Http404()

    host.ip = ip or client_ip
    host.update_time = now()
    host.save()

    return HttpResponse("OK")
