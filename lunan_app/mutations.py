import graphene
import jwt
from .resolvers import UserModel
from .models import User
from .exceptions import AuthenticationError
from django.conf import settings
from django.utils import timezone
from argon2 import PasswordHasher, exceptions as argon2_exceptions
from datetime import datetime, timedelta

ph = PasswordHasher()

def hash_password(password: str)->str:
    return ph.hash(password)

class CreateUserInput(graphene.InputObjectType):
    first_name = graphene.String(required=True)
    last_name = graphene.String(required=True)
    password = graphene.String(required=True)
    email = graphene.String(required=True)
    contact_no = graphene.String(required=True)


class LoginUserInput(graphene.InputObjectType):
    email = graphene.String(required=True)
    password = graphene.String(required=True)


class CreateUser(graphene.Mutation):
    class Arguments:
        create_user = CreateUserInput(required=True)

    user = graphene.Field(UserModel)

    @staticmethod
    def mutate(root, info, create_user):
        hashed_password = ph.hash(create_user.password)
        user = User(
            first_name=create_user.first_name,
            last_name=create_user.last_name,
            password=hashed_password,
            email=create_user.email,
            contact_no=create_user.contact_no,
        )
        user.save()

        return CreateUser(user=user)


class LoginUser(graphene.Mutation):
    class Arguments:
        login_user = LoginUserInput(required=True)

    user = graphene.Field(UserModel)
    token = graphene.String()

    @staticmethod
    def mutate(root, info, login_user):
        now = timezone.now()
        try:
            user = User.objects.get(email=login_user.email)
        except User.DoesNotExist:
            raise AuthenticationError("Invalid Credentials")

        try:
            ph.verify(user.password, login_user.password)
        except argon2_exceptions.VerificationError:
            raise AuthenticationError("Invalid Credentials")

        payload = {
            "user_id": user.id,
            "issued_at": int(now.timestamp()),
            "expired_at": int((now + timedelta(seconds=settings.JWT_EXP_DELTA_SECONDS)).timestamp()),
        }

        token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

        return LoginUser(user=user, token=token)