import graphene
import factory.schema

class Query(factory.schema.Query, graphene.ObjectType):
    pass

class Mutation(factory.schema.Mutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)

