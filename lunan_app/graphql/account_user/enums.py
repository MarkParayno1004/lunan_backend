import graphene


class RoleEnum(graphene.Enum):
    ADMIN = "admin"
    COUNSELOR = "counselor"
    PATIENT = "patient"