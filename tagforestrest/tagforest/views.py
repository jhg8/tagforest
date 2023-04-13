from django.http import HttpResponse
from .models import Tag, TagCategory, Graph
from .serializers import TagSerializer, TagCategorySerializer, ExtendedTagSerializer
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.reverse import reverse
import json

from urllib.parse import parse_qs

class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        kwargs = {
            'user': self.request.user
        }
        serializer.save(**kwargs)

    def get_queryset(self):
        return Tag.objects.filter(user=self.request.user)

class ExtendedTagViewSet(viewsets.ModelViewSet):
    serializer_class = ExtendedTagSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        kwargs = {
            'user': self.request.user
        }
        serializer.save(**kwargs)

    def get_queryset(self):
        return Tag.objects.filter(user=self.request.user)

class TagCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = TagCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        kwargs = {
            'user': self.request.user
        }
        serializer.save(**kwargs)

    def get_queryset(self):
        return TagCategory.objects.filter(user=self.request.user)

@api_view(['GET'])
def root_view(request):
    data = {
                'tags': reverse('tag-list', request=request),
                'tagcategories': reverse('tagcategory-list', request=request),
                'graph': reverse('graph', request=request),
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
@permission_classes([permissions.IsAuthenticated])
def graph_view(request):

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
                tag_set.append(graph.filterTagSet(set([token])))
                query_tag_set.append(token)
                i += 1
        return query[0], tag_set[0], Tag.objects.filter(user=request.user, name__in=query_tag_set)

    import time
    T = []
    T.append(time.time())
    data = {}
    graph = Graph(request.user)
    tag_query, category_query = '', ''
    T.append(time.time())

    if 'q' in request.query_params:
        q = request.query_params['q'].strip()

        q_split = q.split(';', 2)
        tag_query = q_split[0]
        if len(q_split) > 1:
            category_query, tag_query = q_split

    T.append(time.time())
    if tag_query:
        output_queue = shunting_yard(tag_query)
        query_json, tag_set, query_tag_set = process(output_queue, graph)
    else:
        query_json = {}
        tag_set = graph.all
        query_tag_set = Tag.objects.none()

    category_list = TagCategory.objects.filter(user=request.user)
    tag_list = Tag.objects.filter(user=request.user, name__in=tag_set)
    if category_query:
        tag_list = tag_list.filter(category__name=category_query)
        tag_set = set([tag.name for tag in tag_list])

    T.append(time.time())
    control_tag_set = graph.relatedTagSet(tag_set)

    T.append(time.time())
    control_tag_list = [(len(graph.filterTagSet(set([t]))), t) for t in control_tag_set]
    control_tag_list = list(filter(lambda x: x[0] > 1, control_tag_list))
    control_tag_list = sorted(control_tag_list, reverse=True)
    control_tag_list = list(map(lambda x: x[1], control_tag_list))
    control_tag_list = [Tag.objects.filter(user=request.user, name=t).first() for t in control_tag_list]
    T.append(time.time())

    T.append(time.time())

    for i in range(len(T)-1):
        print("T{} - T{}: {}".format(i+1, i, (T[i+1] - T[i]) * 1000))

    data['category_list']    = TagCategorySerializer(category_list, many=True, context = { 'request': request }).data
    data['control_tag_list'] = TagSerializer(control_tag_list,      many=True, context = { 'request': request }).data
    data['tag_list']         = TagSerializer(tag_list,              many=True, context = { 'request': request }).data
    data['query']            = query_json

    return Response(data)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def export_data(request):

    data = {}
    category_list = TagCategory.objects.all().filter(user=request.user)
    tag_list = Tag.objects.all().filter(user=request.user)
    data['export_value'] = {
            'category_list': TagCategorySerializer(category_list, many=True, context = { 'request': request }).data,
            'tag_list': TagSerializer(tag_list, many=True, context = { 'request': request }).data
    }
    return Response(data)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def import_data(request):

    try:
        data = json.loads(request.data['import_value'])

        Tag.objects.all().delete()
        TagCategory.objects.all().delete()

        for category in data['category_list']:
            TagCategory.objects.create(name=category['name'], color=category['color'], user=request.user)

        for tag in data['tag_list']:
            Tag.objects.create(name=tag['name'], category=TagCategory.objects.get(name=tag['category']['name']), user=request.user)

        for tag in data['tag_list']:
            tag_object = Tag.objects.get(name=tag['name'], user=request.user)
            for parent in tag['parent_set']:
                tag_object.parent_set.add(Tag.objects.get(name=parent['name']))
            tag_object.save()

    except json.decoder.JSONDecodeError:
        return Response({'error': 'Invalid JSON'})
    except KeyError:
        return Response({'error': 'Key Error'})

    return Response({})
