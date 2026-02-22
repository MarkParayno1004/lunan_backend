import graphene


class UserModel(graphene.ObjectType):
    first_name = graphene.String()
    last_name = graphene.String()
    password = graphene.String()
    email = graphene.String()
    contact_no = graphene.String()

