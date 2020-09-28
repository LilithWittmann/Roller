import json

from django.http import HttpResponse
from django.http import Http404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from vehicles.management.commands.crawl_vehicles import import_crawler
from vehicles.models import ReceivedSMS, ServiceTrackingArea, ServiceProvider


def home(request):
    return HttpResponse("🎉 Hey there! 🎉", content_type='text/plain; charset=utf-8')


@api_view(['POST'])
def receive_sms(request):
    data = ReceivedSMS.objects.create(content=request.body.decode('utf-8'))
    for service in ServiceProvider.objects.all():
        crawler_cls = import_crawler(service.crawler)
        crawler = crawler_cls(service.settings)
        if "sms_hook" in dir(crawler):
            crawler.sms_hook(service, json.loads(data.content)["Body"])
    return Response(status=status.HTTP_201_CREATED)

