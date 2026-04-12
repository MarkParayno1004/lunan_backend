from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.middleware.csrf import get_token
from django.http import JsonResponse
from .models import User
from .services import TwilioService

# Create your views here.
def say_hello(request):
    return render(request, 'hello.html')

def query_user(request):
    users = User.objects.all().values()  # returns a queryset of dicts
    return JsonResponse(list(users), safe=False)

@ensure_csrf_cookie
def csrf_token_view(request):
    token = get_token(request)
    return JsonResponse({"detail": "CSRF cookie set", "csrfToken": token})

def twilio_token_view(request):
    """Generates an access token for Twilio Conversations for the current user."""
    # Assuming authentication is handled and request.user is populated
    # For now, let's assume we can pass a user_id for development or get from session
    if not request.user.is_authenticated:
         # For demo purposes, we'll try to get it from request params if not authenticated
         user_email = request.GET.get('email', 'guest@example.com')
         user_role = 'guest'
    else:
         user_email = request.user.email
         # Assuming user model has role or we fetch from Profile/Counselor/Patient
         user_role = getattr(request.user, 'role', 'patient')

    token_data = TwilioService.generate_chat_access_token(user_email, user_role)
    return JsonResponse(token_data)