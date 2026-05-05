import graphene
import factory.schema

class Query(factory.schema.Query, graphene.ObjectType):
    pass

class Mutation(graphene.ObjectType):
    pass

shema = graphene.Schema(query=Query, mutation=Mutation)

