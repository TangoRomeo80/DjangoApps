from django.core.mail import send_mail, mail_admins, BadHeaderError, EmailMessage
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from templated_mail.mail import BaseEmailMessage
from django.utils.decorators import method_decorator
import requests
from rest_framework.views import APIView
import logging
# from .tasks import notify_customers


logger = logging.getLogger(__name__)

# Caching a class based view
class HelloView(APIView):
    # @method_decorator(cache_page(10 * 60))
    def get(self, request):
        try:
            logger.info('Calling httpbin')
            response = requests.get('https://httpbin.org/delay/2')
            logger.info('Got response from httpbin')
            data = response.json()
        except request.ConnectionError:
            logger.critical('Httpbin is offline')
        return render(request, 'hello.html', {'name': data})


# @cache_page(10 * 60)  # Caching the view for 10 minutes
# def say_hello(request):
    # notify_customers.delay('Hello World')
    # try:
    # send mail to users
    # send_mail('Subject here', 'Here is the message.', 'admin@localhost.com', [
    #     'bob@localhost.com',
    # ])

    # send mail to admins
    # mail_admins('Subject here', 'Here is the message.', html_message='<h1>Message</h1>')

    # send mail with attachements
    # message = EmailMessage(
    #     'Subject here',
    #     'Here is the message.',
    #     'from@localhost.com',
    #     ['john@localhost.com'],)
    # message.attach_file('playground/static/images/dog.png')
    # message.send()

    # send mail with template
    #     message = BaseEmailMessage(
    #         template_name='emails/hello.html',
    #         context={
    #             'name': 'Mosh'
    #         }
    #     )
    #     message.send(['mosh@localhost.com'])

    # except BadHeaderError:
    #     pass
    # Simulate a slow API

    # Low level caching
    # key = 'httpbin_result'
    # if cache.get(key) is None:
    #     response = requests.get('https://httpbin.org/delay/2')
    #     data = response.json()
    #     cache.set(key, data)

    # High level caching with decorators
    # response = requests.get('https://httpbin.org/delay/2')
    # data = response.json()

    # return render(request, 'hello.html', {'name': data})
