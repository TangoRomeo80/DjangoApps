from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product



def say_hello(request):
    
    
    return render(request, 'hello.html', {'name': 'Mosh'})
