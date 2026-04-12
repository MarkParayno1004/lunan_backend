import graphene
import jwt
from .graphql.account_user.models import CreateUserInput, LoginUserInput, UserModel
from .models import User
from django.conf import settings
from django.utils import timezone
from argon2 import PasswordHasher, exceptions as argon2_exceptions
from datetime import timedelta
from graphql import GraphQLError

ph = PasswordHasher()

def hash_password(password: str)->str:
    return ph.hash(password)


class CreateUser(graphene.Mutation):
    class Arguments:
        create_user = CreateUserInput(required=True)

    user = graphene.Field(UserModel)

    @staticmethod
    def mutate(root, info, create_user):
        hashed_password = ph.hash(create_user.password)
        role_value = create_user.role.value if create_user.role else None
        user = User(
            first_name=create_user.first_name,
            last_name=create_user.last_name,
            password=hashed_password,
            email=create_user.email,
            contact_no=create_user.contact_no,
            role=role_value,
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
        email = login_user.email.strip().lower()

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise GraphQLError("User Does Not Exist")

        password_ok = False

        # Accept both current Argon2 hashes and legacy plain-text passwords.
        # If legacy password matches, upgrade it to Argon2 immediately.
        if user.password and user.password.startswith("$argon2"):
            try:
                password_ok = ph.verify(user.password, login_user.password)
                if ph.check_needs_rehash(user.password):
                    user.password = ph.hash(login_user.password)
                    user.save(update_fields=["password"])
            except (argon2_exceptions.VerificationError, argon2_exceptions.InvalidHashError):
                password_ok = False
        else:
            if user.password == login_user.password:
                password_ok = True
                user.password = ph.hash(login_user.password)
                user.save(update_fields=["password"])

        if not password_ok:
            raise GraphQLError("Invalid credentials")

        payload = {
            "user_id": user.id,
            "issued_at": int(now.timestamp()),
            "expired_at": int((now + timedelta(seconds=settings.JWT_EXP_DELTA_SECONDS)).timestamp()),
        }

        token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

        return LoginUser(user=user, token=token)