import graphene
import lunan_app.schema

class Query(lunan_app.schema.Query, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query)
