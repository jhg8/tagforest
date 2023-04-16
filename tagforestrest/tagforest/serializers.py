from rest_framework import serializers
from django.contrib.auth.models import User, Group
from django.contrib.auth.validators import UnicodeUsernameValidator
from .models import Tag, TagCategory, Graph

class TagCategorySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = TagCategory
        fields = ['id', 'url', 'name', 'color']
        extra_kwargs = {
            'name': {
                'validators': [],
            },
        }

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        tag_category = TagCategory.objects.create(name=validated_data.pop('name'), color=validated_data.pop('color'), user=user_data)
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

    class Meta:
        model = Tag
        fields = ['id', 'url', 'name', 'category']
        extra_kwargs = {
            'name': {
                'validators': [],
            },
        }

class TagSerializer(serializers.HyperlinkedModelSerializer):
    parent_set = SimpleTagSerializer(many=True)
    category = TagCategorySerializer()

    class Meta:
        model = Tag
        fields = ['id', 'url', 'name', 'category', 'parent_set', 'content']
        extra_kwargs = {
            'name': {
                'validators': [],
            },
        }

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        category = TagCategory.objects.get_or_create(name=validated_data.pop('category')['name'], user=user_data)[0]
        tag = Tag.objects.create(name=validated_data.pop('name'), category=category, content=validated_data.pop('content'), user=user_data)
        for tag_data in validated_data.pop('parent_set'):
            parent_category = TagCategory.objects.get_or_create(name=tag_data['category']['name'], user=user_data)[0]
            tag.parent_set.add(Tag.objects.get_or_create(name=tag_data['name'], category=parent_category, user=user_data)[0])
        tag.save()
        tag.clean()
        return tag

    def update(self, tag, validated_data):
        tag.name = validated_data.pop('name')
        tag.category = TagCategory.objects.get_or_create(name=validated_data.pop('category')['name'], user=tag.user)[0]
        tag.content = validated_data.pop('content')
        tag.parent_set.clear()
        for tag_data in validated_data.pop('parent_set'):
            parent_category = TagCategory.objects.get_or_create(name=tag_data['category']['name'], user=tag.user)[0]
            tag.parent_set.add(Tag.objects.get_or_create(name=tag_data['name'], category=parent_category, user=tag.user)[0])
        tag.save()
        tag.clean()
        return tag

class ExtendedTagSerializer(TagSerializer):
    extended_parent_set = serializers.SerializerMethodField()

    class Meta:
        model = Tag
        fields = ['id', 'url', 'name', 'category', 'parent_set', 'content', 'extended_parent_set']
        read_only_fields = ['extended_parent_set']
        extra_kwargs = {
            'name': {
                'validators': [],
            },
        }

    def get_extended_parent_set(self, obj):
        graph = Graph(obj.user)
        return SimpleTagSerializer(Tag.objects.filter(user=obj.user, name__in=graph.extendedAscendantSet(set([obj.name]))), many=True, context=self.context).data

