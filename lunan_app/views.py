from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse
from .models import User

# Create your views here.
def say_hello(request):
    return render(request, 'hello.html')

def query_user(request):
    users = User.objects.all().values()  # returns a queryset of dicts
    return JsonResponse(list(users), safe=False)

@ensure_csrf_cookie
def csrf_token_view(request):
    return JsonResponse({"detail": "CSRF cookie set"})