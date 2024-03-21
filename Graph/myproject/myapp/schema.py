import graphene
from graphene_django.types import DjangoObjectType
from .models import Item

class ItemType(DjangoObjectType):
    class Meta:
        model = Item
        fields = "__all__"

class Query(graphene.ObjectType):
    all_items = graphene.List(ItemType)
    test = graphene.List(ItemType)

    def resolve_all_items(root, info):
        return Item.objects.all()

    def resolve_test(root, info):
        return Item.objects.filter(name__icontains="e")

schema = graphene.Schema(query=Query)
