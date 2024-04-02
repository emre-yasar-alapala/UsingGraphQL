import graphene
from graphene_django.types import DjangoObjectType
from .models import Item, Category

class ItemType(DjangoObjectType):
    class Meta:
        model = Item
        fields = "__all__"
        
class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = "__all__"

class Query(graphene.ObjectType):
    all_items = graphene.List(ItemType)
    test = graphene.List(ItemType)
    all_categories = graphene.List(CategoryType)
    category_by_name = graphene.Field(CategoryType, name=graphene.String(required=True))

    def resolve_all_items(root, info):
        return Item.objects.all()

    def resolve_test(root, info):
        return Item.objects.filter(name__icontains="e")
    


    def resolve_all_categories(root, info):
        return Category.objects.select_related("items").all()

    def resolve_category_by_name(root, info, name):
        try:
            return Category.objects.get(name=name)
        except Category.DoesNotExist:
            return None


class CreateItem(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String(required=True)

    item = graphene.Field(ItemType)

    @staticmethod
    def mutate(root, info, name, description):
        item = Item(name=name, description=description)
        item.save()
        return CreateItem(item=item)
    
class UpdateItem(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String()
        description = graphene.String()

    item = graphene.Field(ItemType)

    @staticmethod
    def mutate(root, info, id, name=None, description=None):
        item = Item.objects.get(pk=id)
        
        if name is not None:
            item.name = name
        if description is not None:
            item.description = description

        item.save()
        return UpdateItem(item=item)

class DeleteItem(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    @staticmethod
    def mutate(root, info, id):
        item = Item.objects.get(pk=id)
        item.delete()
        return DeleteItem(success=True)
class Mutation(graphene.ObjectType):
    create_item = CreateItem.Field()
    update_item = UpdateItem.Field()
    delete_item = DeleteItem.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
