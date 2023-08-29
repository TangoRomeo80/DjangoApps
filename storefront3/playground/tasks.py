# Tasks to test the Celery worker
from time import sleep
# from storefront.celery import celery
from celery import shared_task

# @celery.task
@shared_task
def notify_customers(message):
    print('Sending message to 10k customers: ')
    print(message)
    sleep(10)
    print('Emails successfully sent!')
