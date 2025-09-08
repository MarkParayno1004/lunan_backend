from django.shortcuts import render
from django.http import JsonResponse
from .models import User

# Create your views here.
def say_hello(request):
    return render(request, 'hello.html')

def query_user(request):
    users = User.objects.all().values()  # returns a queryset of dicts
    return JsonResponse(list(users), safe=False)