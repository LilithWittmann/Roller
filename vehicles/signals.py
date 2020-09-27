from django.dispatch import receiver
from django.db.models.signals import post_save

### Define your signals here.
# EXAMPLE:
# @receiver(post_save, sender=SomeModel)
# def do_something_at_post_save(instance, ...):
#     ...

from eb_sqs_worker.decorators import task
from django.core import management

from vehicles.models import PingModel


@task(task_name="crawl_vehicles_crontask")
def crawl_vehicles_task(**kwargs):
    management.call_command('crawl_vehicles')
    return True

@task(task_name="ping_test")
def ping_pong(**kwargs):
    PingModel.objects.create()
    return True