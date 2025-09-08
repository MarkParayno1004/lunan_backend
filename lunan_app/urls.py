from django.urls import path
from graphene_django.views import GraphQLView
from lunan_app.schema import schema
from . import views

urlpatterns = [
    path('hello/', views.say_hello),
    path('query_users/', views.query_user),
    path('graphql/', GraphQLView.as_view(graphiql=True, schema=schema)),
]