from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Tree, Tag, TagCategory, Graph
from .serializers import TreeSerializer, TagSerializer, SimpleTagSerializer, TagCategorySerializer, ExtendedTagSerializer
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, BasePermission
from rest_framework import viewsets, mixins
from rest_framework.decorators import api_view, action, permission_classes
from rest_framework.exceptions import PermissionDenied
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.reverse import reverse
import json

from urllib.parse import parse_qs

class TreeReadPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if (not obj.public) and (request.user != obj.user):
          raise PermissionDenied({"message": "You are not allowed to see this tree, sorry"})
        return True

class TreeWritePermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user != obj.user:
          raise PermissionDenied({"message": "You are not allowed to see this tree"})
        return True

class TreeViewSet(viewsets.ModelViewSet):
    serializer_class = TreeSerializer

    def get_queryset(self):
        if self.action == 'list':
            return Tree.objects.filter(user=self.request.user).all()
        return Tree.objects.all()

    def get_permissions(self):
        if self.action in ['retrieve', 'tag_list', 'tag_category_list']:
            permission_classes = [TreeReadPermission]
        elif self.action in ['update', 'destroy']:
            permission_classes = [TreeWritePermission]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        kwargs = {
            'user': self.request.user
        }
        serializer.save(**kwargs)

    @action(detail=True)
    def tag_list(self, request, pk=None):
      tree = self.get_object()
      tag_list = Tag.objects.filter(user=tree.user, tree=tree)
      return Response(TagSerializer(tag_list, many = True, context = { 'request': request }).data)

    @action(detail=True)
    def tag_category_list(self, request, pk=None):
      tree = self.get_object()
      tag_category_list = TagCategory.objects.filter(user=tree.user, tree=tree)
      return Response(TagCategorySerializer(tag_category_list, many = True, context = { 'request': request }).data)

class TreeChildReadPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if (not obj.tree.public) and (request.user != obj.tree.user):
          raise PermissionDenied({"message": "You are not allowed to see this tree"})
        return True

class TreeChildWritePermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user != obj.tree.user:
          raise PermissionDenied({"message": "You are not allowed to see this tree"})
        return True

class TreeChildBaseViewSet(mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):

    def get_permissions(self):
        if self.action == 'retrieve':
            permission_classes = [TreeChildReadPermission]
        elif self.action in ['update', 'destroy']:
            permission_classes = [TreeChildWritePermission]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

class TagViewSet(TreeChildBaseViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()

    def perform_create(self, serializer):
        kwargs = {
            'user': self.request.user
        }
        serializer.save(**kwargs)

class ExtendedTagViewSet(TreeChildBaseViewSet):
    serializer_class = ExtendedTagSerializer
    queryset = Tag.objects.all()

    def perform_create(self, serializer):
        kwargs = {
            'user': self.request.user
        }
        serializer.save(**kwargs)

class TagCategoryViewSet(TreeChildBaseViewSet):
    serializer_class = TagCategorySerializer
    queryset = TagCategory.objects.all()

    def perform_create(self, serializer):
        kwargs = {
            'user': self.request.user
        }
        serializer.save(**kwargs)

@api_view(['GET'])
def root_view(request):
    data = {
                'trees': reverse('tree-list', request=request),
    }
    return Response(data)

# Returns partial graph based on a query
#
# Query: 'q' URL query string,
#        arithmetic expression with ^ ('and') and | ('or) operators
# Example: ?q=(Tag 1 ^ Tag 2) | Tag 3
#          = (Tag 1 and Tag 2) or Tag 3
#
# Returns:
#   - category_list
#   - tag_list:         Tags matching the query
#   - control_tag_list: Tags whose child set intersects tag_list
#   - query:            JSON representation of the query
@api_view(['GET'])
def graph_view(request, tree_pk):

    # Shunting-Yard algorithm (Operator precedence parser)
    def shunting_yard(q):
        output_queue = list()
        operator_stack = list()
        i, n = 0, len(q)
        try:
            while i < n:
                c = q[i]
                if c == ' ':
                    i += 1
                    continue
                if c == '^':
                    operator_stack.append(c)
                elif c == '|':
                    while operator_stack and operator_stack[-1] == '^':
                        output_queue.append(operator_stack.pop())
                    operator_stack.append(c)
                elif c == '(':
                    operator_stack.append(c)
                elif c == ')':
                    while operator_stack[-1] != '(':
                        output_queue.append(operator_stack.pop())
                    operator_stack.pop()
                else:
                    j = i
                    while j < n and q[j] not in "^|()":
                        j += 1
                    w = q[i:j]
                    i = j - 1
                    output_queue.append(w.strip())
                i += 1
            while operator_stack:
                if operator_stack[-1] == '(':
                    return False
                output_queue.append(operator_stack.pop())
        except IndexError:
            return False
        return output_queue

    # TODO : Use graph algorithms instead of query unions and intersections
    def process(output_queue, graph):
        query = []
        query_tag_set = []
        tag_set = []
        n = len(output_queue)
        i = 0
        while i < n:
            token = output_queue[i]
            if token in '^|':
                l = 0
                while (i + l) < n and output_queue[i + l] == token:
                    l += 1
                if len(query) < l + 1 or len(tag_set) < l + 1:
                    return False
                if token == '^':
                    query.append({ 'intersection': [query.pop() for j in range(l + 1)] })
                    tag_set.append(tag_set.pop().intersection(*[tag_set.pop() for j in range(l)]))
                else:
                    query.append({ 'union': [query.pop() for j in range(l + 1)] })
                    tag_set.append(tag_set.pop().union(*[tag_set.pop() for j in range(l)]))
                i += l
            else:
                query.append({ 'tag': token })
                tag_set.append(graph.extendedDescendantSet(set([token])))
                query_tag_set.append(token)
                i += 1
        return query[0], tag_set[0], tag_queryset.filter(name__in=query_tag_set)

    data = {}

    tree = get_object_or_404(Tree, pk=tree_pk)
    if (not tree.public) and (request.user != tree.user):
        raise PermissionDenied({"message": "You are not allowed to see this tree"})

    graph = Graph(tree.user, tree=tree)
    tag_query, category_query = '', ''
    tag_queryset = Tag.objects.filter(user=tree.user, tree__pk=tree_pk)
    tag_category_queryset = TagCategory.objects.filter(user=tree.user, tree__pk=tree_pk)

    if 'q' in request.query_params:
        q = request.query_params['q'].strip()

        q_split = q.split(';', 2)
        tag_query = q_split[0]
        if len(q_split) > 1:
            category_query, tag_query = q_split

    if tag_query:
        output_queue = shunting_yard(tag_query)
        query_json, tag_set, query_tag_set = process(output_queue, graph)
    else:
        query_json = {}
        tag_set = graph.all
        query_tag_set = Tag.objects.none()

    tag_list = tag_queryset.filter(name__in=tag_set)

    category_set = set()
    hidden_category_set = set()
    for category in tag_category_queryset.all():
        (category_set if category.show_in_results else hidden_category_set).add(category.name)
    if category_query:
        result_category_set = set([category_query])
    else:
        result_category_set = category_set

    tag_list = tag_list.filter(category__name__in=result_category_set)
    tag_set = set([tag.name for tag in tag_list])
    category_list        = tag_category_queryset.filter(name__in=category_set)
    hidden_category_list = tag_category_queryset.filter(name__in=hidden_category_set )

    control_tag_set = graph.extendedAscendantSet(tag_set)

    control_category_set = set()
    for category in tag_category_queryset.all():
        if category.use_as_filter:
            control_category_set.add(category.name)

    _control_tag_list = [(len(graph.extendedDescendantSet(set([t]))), t) for t in control_tag_set]
    _control_tag_list = list(filter(lambda x: x[0] > 1, _control_tag_list))
    _control_tag_list = sorted(_control_tag_list, reverse=True)
    _control_tag_list = list(map(lambda x: x[1], _control_tag_list))
    control_tag_list = []
    for t in _control_tag_list:
        q = tag_queryset.filter(name=t, category__name__in=control_category_set)
        if q:
            control_tag_list.append(q.first())

    data['tree_name'] = tree.name
    data['hidden_category_list'] = TagCategorySerializer(hidden_category_list, many=True, context = { 'request': request }).data
    data['category_list']        = TagCategorySerializer(category_list,        many=True, context = { 'request': request }).data
    data['control_tag_list']     = SimpleTagSerializer(control_tag_list,       many=True, context = { 'request': request }).data
    data['tag_list']             = SimpleTagSerializer(tag_list,               many=True, context = { 'request': request }).data
    data['full_tag_list']        = SimpleTagSerializer(tag_queryset,           many=True, context = { 'request': request }).data
    data['query']                = query_json

    return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def export_data(request, tree_pk):

    data = {}
    tag_category_queryset = TagCategory.objects.filter(user=request.user, tree__pk=tree_pk)
    tag_queryset = Tag.objects.filter(user=request.user, tree__pk=tree_pk)
    data['export_value'] = {
            'category_list': TagCategorySerializer(tag_category_queryset, many=True, context = { 'request': request }).data,
            'tag_list': TagSerializer(tag_queryset, many=True, context = { 'request': request }).data
    }
    return Response(data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def import_data(request, tree_pk):

    try:
        data = json.loads(request.data['import_value'])

        tree = Tree.objects.get(pk=tree_pk, user=request.user)
        tag_category_queryset = TagCategory.objects.filter(user=request.user, tree=tree)
        tag_queryset = Tag.objects.filter(user=request.user, tree=tree)

        tag_queryset.delete()
        tag_category_queryset.delete()

        for category in data['category_list']:
            TagCategory.objects.create(name=category['name'], color=category['color'], tree=tree, user=request.user)

        for tag in data['tag_list']:
            Tag.objects.create(
                    name=tag['name'], 
                    category=TagCategory.objects.get(name=tag['category']['name'], tree=tree, user=request.user),
                    user=request.user,
                    tree=tree,
            )

        for tag in data['tag_list']:
            tag_object = Tag.objects.get(name=tag['name'], tree=tree, user=request.user)
            for parent in tag['parent_set']:
                tag_object.parent_set.add(Tag.objects.get(name=parent['name'], tree=tree, user=request.user))
            tag_object.save()

    except json.decoder.JSONDecodeError:
        return Response({'error': 'Invalid JSON'})
    except KeyError:
        return Response({'error': 'Key Error'})

    return Response({})
