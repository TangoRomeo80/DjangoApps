from django.core.mail import send_mail, mail_admins, BadHeaderError
from django.shortcuts import render


def say_hello(request):
    try:
        # send mail to users
        # send_mail('Subject here', 'Here is the message.', 'admin@localhost.com', [
        #     'bob@localhost.com',
        # ])

        # send mail to admins
        mail_admins('Subject here', 'Here is the message.', html_message='<h1>Message</h1>')
    except BadHeaderError:  
        pass
    return render(request, 'hello.html', {'name': 'Mosh'})
