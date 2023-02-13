from rest_framework import serializers
from django.contrib.auth.models import User, Group
from django.contrib.auth.validators import UnicodeUsernameValidator
from .models import Tag

class SimpleTagSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Tag
        fields = ['id', 'url', 'name']
        extra_kwargs = {
            'name': {
                'validators': [],
            },
        }

class TagSerializer(serializers.HyperlinkedModelSerializer):
    parent_set = SimpleTagSerializer(many=True)

    class Meta:
        model = Tag
        fields = ['id', 'url', 'name', 'parent_set', 'content']
        extra_kwargs = {
            'name': {
                'validators': [],
            },
        }

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        tag = Tag.objects.create(name=validated_data.pop('name'), content=validated_data.pop('content'), user=user_data)
        for tag_data in validated_data.pop('parent_set'):
            tag.parent_set.add(Tag.objects.get_or_create(name=tag_data['name'], user=user_data)[0])
        tag.save()
        tag.clean()
        return tag

    def update(self, tag, validated_data):
        tag.name = validated_data.pop('name')
        tag.content = validated_data.pop('content')
        tag.parent_set.clear()
        for tag_data in validated_data.pop('parent_set'):
            tag.parent_set.add(Tag.objects.get_or_create(name=tag_data['name'], user=tag.user)[0])
        tag.save()
        tag.clean()
        return tag
