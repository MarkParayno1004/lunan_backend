import graphene
from graphene_django import DjangoObjectType
from .models import User

class UserModel(DjangoObjectType):
    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "contact_no",
        )

class Query(graphene.ObjectType):
    users = graphene.List(UserModel)

    def resolve_users(self, info, **kwargs):
        return User.objects.all()

schema = graphene.Schema(query=Query)