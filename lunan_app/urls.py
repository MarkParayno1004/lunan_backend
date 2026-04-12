from django.urls import path
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import ensure_csrf_cookie
from lunan_app.schema import schema
from . import views

urlpatterns = [
    path('hello/', views.say_hello),
    path('query_users/', views.query_user),
    path('graphql/', ensure_csrf_cookie(GraphQLView.as_view(graphiql=True, schema=schema))),
    path("csrf/", views.csrf_token_view),
    path("twilio-token/", views.twilio_token_view),
]