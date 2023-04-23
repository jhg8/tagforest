from rest_framework import serializers
from rest_framework.reverse import reverse
from django.contrib.auth.models import User, Group
from django.contrib.auth.validators import UnicodeUsernameValidator
from .models import Tree, Tag, TagCategory, Graph

class TreeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Tree
        fields = ['id', 'url', 'name']
        extra_kwargs = {
            'name': {
                'validators': [],
            },
        }

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        tree = Tree.objects.create(name=validated_data.pop('name'), user=user_data)
        tree.save()
        tree.clean()
        return tree

    def update(self, tree, validated_data):
        tree.name = validated_data.pop('name')
        tree.save()
        tree.clean()
        return tree

class TagCategorySerializer(serializers.HyperlinkedModelSerializer):

    tree = TreeSerializer()

    class Meta:
        model = TagCategory
        fields = ['id', 'url', 'name', 'color', 'tree']
        extra_kwargs = {
            'name': {
                'validators': [],
            },
        }

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        tree = Tree.objects.get(name=validated_data.pop('tree')['name'], user=user_data)
        tag_category = TagCategory.objects.create(
                name=validated_data.pop('name'), 
                color=validated_data.pop('color'), 
                user=user_data,
                tree=tree,
        )
        tag_category.save()
        tag_category.clean()
        return tag_category

    def update(self, tag_category, validated_data):
        tag_category.name = validated_data.pop('name')
        tag_category.color = validated_data.pop('color')
        tag_category.save()
        tag_category.clean()
        return tag_category

class SimpleTagSerializer(serializers.HyperlinkedModelSerializer):

    category = TagCategorySerializer()
    tree = TreeSerializer()

    class Meta:
        model = Tag
        fields = ['id', 'url', 'name', 'category', 'tree']
        extra_kwargs = {
            'name': {
                'validators': [],
            },
        }

class TagSerializer(serializers.HyperlinkedModelSerializer):
    parent_set = SimpleTagSerializer(many=True)
    category = TagCategorySerializer()
    tree = TreeSerializer()

    class Meta:
        model = Tag
        fields = ['id', 'url', 'name', 'category', 'parent_set', 'content', 'tree']
        extra_kwargs = {
            'name': {
                'validators': [],
            },
        }

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        tree = Tree.objects.get(name=validated_data.pop('tree')['name'], user=user_data)
        create_args = {
            'name': validated_data.pop('name'),
            'category': TagCategory.objects.get(name=validated_data.pop('category')['name'], tree=tree, user=user_data),
            'tree': tree,
            'user': user_data,
        }
        if 'content' in validated_data:
          create_args['content'] = validated_data.pop('content')
        tag = Tag.objects.create(**create_args)
        for tag_data in validated_data.pop('parent_set'):
            tag.parent_set.add(Tag.objects.get(name=tag_data['name'], tree=tree, user=user_data))
        tag.save()
        tag.clean()
        return tag

    def update(self, tag, validated_data):
        tag.name = validated_data.pop('name')
        tag.category = TagCategory.objects.get(name=validated_data.pop('category')['name'], tree=tag.tree, user=tag.user)
        if 'content' in validated_data:
          tag.content = validated_data.pop('content')
        tag.parent_set.clear()
        for tag_data in validated_data.pop('parent_set'):
            tag.parent_set.add(Tag.objects.get(name=tag_data['name'], tree=tag.tree, user=tag.user))
        tag.save()
        tag.clean()
        return tag

class ExtendedTagSerializer(TagSerializer):
    extended_parent_set = serializers.SerializerMethodField()

    class Meta:
        model = Tag
        fields = ['id', 'url', 'name', 'category', 'parent_set', 'content', 'tree', 'extended_parent_set']
        read_only_fields = ['extended_parent_set']
        extra_kwargs = {
            'name': {
                'validators': [],
            },
        }

    def get_extended_parent_set(self, obj):
        graph = Graph(obj.user, obj.tree)
        extended_ascendant_set = graph.extendedAscendantSet(set([obj.name]))
        parent_set = graph.graph[obj.name]
        return SimpleTagSerializer(Tag.objects.filter(user=obj.user, tree=obj.tree, name__in=extended_ascendant_set.difference(parent_set)), many=True, context=self.context).data
