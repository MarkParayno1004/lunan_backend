import jwt
from django.conf import settings
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.middleware.csrf import get_token
from django.http import JsonResponse
from .models import User
from .services.twilio_service import TwilioService

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

@csrf_exempt
def twilio_token_view(request):
    """Generates an access token for Twilio Conversations for the current user using JWT auth."""
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return JsonResponse({'error': 'Authorization header missing or invalid'}, status=401)

    token = auth_header.split(' ')[1]
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        user_id = payload.get('user_id')
        user = User.objects.get(id=user_id)
        
        identity = user.email
        user_role = user.role or 'patient'
        
        token_data = TwilioService.generate_chat_access_token(identity, user_role)
        return JsonResponse(token_data)
    except jwt.ExpiredSignatureError:
        return JsonResponse({'error': 'Token expired'}, status=401)
    except jwt.InvalidTokenError:
        return JsonResponse({'error': 'Invalid token'}, status=401)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)