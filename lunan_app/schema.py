import graphene
from graphene_django import DjangoObjectType
from .models import User
from .mutations import CreateUser, LoginUser

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


class Mutations(graphene.ObjectType):
    create_user = CreateUser.Field()
    user_login = LoginUser.Field()


class Query(graphene.ObjectType):
    users = graphene.List(UserModel)

    def resolve_users(self, info, **kwargs):
        return User.objects.all()

schema = graphene.Schema(query=Query, mutation=Mutations)