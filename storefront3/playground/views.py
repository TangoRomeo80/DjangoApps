from django.core.mail import send_mail, mail_admins, BadHeaderError, EmailMessage
from django.shortcuts import render
from templated_mail.mail import BaseEmailMessage
from .tasks import notify_customers


def say_hello(request):
    notify_customers.delay('Hello World')
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
    return render(request, 'hello.html', {'name': 'Mosh'})
