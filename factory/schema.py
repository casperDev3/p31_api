import graphene
from graphene_django.types import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from .models import WorkShop, Worker, Attendance, Shipment

# -- GraphQL Types
class WorkShopType(DjangoObjectType):
    class Meta:
        model = WorkShop
        # fields = '__all__'
        fields = ('id', 'name', 'workers')

class WorkerType(DjangoObjectType):
    class Meta:
        model = Worker
        fields = ('id', 'name', 'position', 'workshop', 'attendances')

# -- GraphQL Nodes
class WorkerNode(DjangoObjectType):
    class Meta:
        model = Worker
        filter_fields = ['name', 'position']
        interfaces = (graphene.relay.Node,)

# --     GraphQL Queries
class Query(graphene.ObjectType):
    all_workers = graphene.List(WorkerType)
    workshop_by_name = graphene.Field(WorkShopType, name=graphene.String(required=True))
    worker_filter = DjangoFilterConnectionField(WorkerNode)

    def resolve_all_workers(root, info):
        return Worker.objects.select_related('workshop').all()

    def resolve_workshop_by_name(root, info, name):
        try:
            return WorkShop.objects.get(name=name)
        except WorkShop.DoesNotExist:
            return None

# --     GraphQL Mutations
class CreateAttendanceMutation(graphene.Mutation):
    class Arguments:
        worker_id = graphene.ID(required=True)

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, worker_id):
        worker = Worker.objects.get(pk=worker_id)
        Attendance.objects.create(worker=worker)
        return CreateAttendanceMutation().success

class Mutation(graphene.ObjectType):
    make_attendance = CreateAttendanceMutation.Field()