import graphene
from django.contrib.messages import success
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
    one_worker = graphene.Field(WorkerType, id=graphene.ID(required=True))

    def resolve_all_workers(root, info):
        return Worker.objects.select_related('workshop').all()

    def resolve_workshop_by_name(root, info, name):
        try:
            return WorkShop.objects.get(name=name)
        except WorkShop.DoesNotExist:
            return None

    def resolve_one_worker(root,  info, id):
        try:
            return Worker.objects.get(pk=id)
        except Worker.DoesNotExist:
            return None

# --     GraphQL Mutations
class CreateAttendanceMutation(graphene.Mutation):
    class Arguments:
        worker_id = graphene.ID(required=True)

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, worker_id):
        worker = Worker.objects.get(pk=worker_id)
        Attendance.objects.create(worker=worker, date=graphene.Date(), clock_in=graphene.Time())
        return CreateAttendanceMutation(success=True)

class CreateWorkerMutation(graphene.Mutation):
    id = graphene.ID(required=True)
    name = graphene.String()
    position = graphene.String()
    workshop = graphene.Field(WorkShopType)

    class Arguments:
        name = graphene.String(required=True)
        position = graphene.String(required=True)
        workshop_id = graphene.ID(required=True)

    @classmethod
    def mutate(cls, root, info, name, position, workshop_id):
        workshop = WorkShop.objects.get(pk=workshop_id)
        worker = Worker.objects.create(name=name, position=position, workshop=workshop)
        return CreateWorkerMutation(
            id=worker.id,
            name=worker.name,
            position=worker.position,
            workshop=workshop
        )

class UpdateWorkerMutation(graphene.Mutation):
    id = graphene.ID(required=True)
    name = graphene.String()
    position = graphene.String()
    workshop = graphene.Field(WorkShopType)

    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String()
        position = graphene.String()
        workshop_id = graphene.ID()

    @classmethod
    def mutate(cls, root, info, id, name=None, position=None, workshop_id=None):
        worker = Worker.objects.get(pk=id)
        if name:
            worker.name = name
        if position:
            worker.position = position
        if workshop_id:
            workshop = WorkShop.objects.get(pk=workshop_id)
            worker.workshop = workshop
        worker.save()
        return UpdateWorkerMutation(
            id=worker.id,
            name=worker.name,
            position=worker.position,
            workshop=worker.workshop
        )

class DeleteWorkerMutation(graphene.Mutation):
    id = graphene.ID(required=True)
    is_deleted = graphene.Boolean()

    class Arguments:
        id = graphene.ID(required=True)

    @classmethod
    def mutate(cls, root, info, id):
        worker = Worker.objects.get(pk=id)
        worker.delete()
        return DeleteWorkerMutation(id=id, is_deleted=True)

class Mutation(graphene.ObjectType):
    make_attendance = CreateAttendanceMutation.Field()
    create_worker = CreateWorkerMutation.Field()
    update_worker = UpdateWorkerMutation.Field()
    delete_worker = DeleteWorkerMutation.Field()