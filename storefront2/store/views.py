from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

# default django built in response
# def product_list(request):
#     return HttpResponse('OK')

# rest framework response
@api_view()
def product_list(request):
    return Response('OK')

@api_view()
def product_detail(request, id):
    return Response(id)