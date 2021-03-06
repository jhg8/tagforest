from django.http import HttpResponse
from .models import Entry, Tag
from .serializers import EntrySerializer, TagSerializer
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse

from urllib.parse import parse_qs

class EntryViewSet(viewsets.ModelViewSet):
    serializer_class = EntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        kwargs = {
            'user': self.request.user
        }
        serializer.save(**kwargs)

    def get_queryset(self):
        return Entry.objects.filter(user=self.request.user)

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

@api_view(['GET'])
def root_view(request):
    data = {
                'entries': reverse('entry-list', request=request),
                'tags': reverse('tag-list', request=request),
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
#   - entry_set:        Entries having at least one tag matching the query
#   - tag_list:         Tags matching the query
#   - entry_tag_list:   Sorted list of tags belonging to entries in entry_set
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
    def process(output_queue):
        query = []
        entry_set = []
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
                if len(query) < l + 1 or len(entry_set) < l + 1 or len(tag_set) < l + 1:
                    return False
                if token == '^':
                    query.append({ 'intersection': [query.pop() for j in range(l + 1)] })
                    entry_set.append(entry_set.pop().intersection(*[entry_set.pop() for j in range(l)]))
                    tag_set.append(tag_set.pop().intersection(*[tag_set.pop() for j in range(l)]))
                else:
                    query.append({ 'union': [query.pop() for j in range(l + 1)] })
                    entry_set.append(entry_set.pop().union(*[entry_set.pop() for j in range(l)]))
                    tag_set.append(tag_set.pop().union(*[tag_set.pop() for j in range(l)]))
                i += l
            else:
                query.append({ 'tag': token })
                tag_query = Tag.objects.filter(user=request.user).filter(name=token)
                tag = Tag.objects.filter(user=request.user).filter(name=token).first()
                entry_set.append(tag.recursiveEntrySet() if tag else Entry.objects.none())
                tag_set.append(tag.recursiveChildSet().union(tag_query) if tag else Tag.objects.none())
                query_tag_set.append(token)
                i += 1
        return query[0], entry_set[0], tag_set[0], Tag.objects.filter(user=request.user).filter(name__in=query_tag_set)

    data = {}

    if 'q' in request.query_params:
        q = request.query_params['q'].strip()

        output_queue = shunting_yard(q)
        query_json, entry_set, tag_list, query_tag_set = process(output_queue)
    else:
        query_json = {}
        entry_set = Entry.objects.filter(user=request.user)
        tag_list = Tag.objects.filter(user=request.user)
        query_tag_set = Tag.objects.none()
    tag_list_queries = []
    for entry in entry_set:
        tag_list_queries += [tag.recursiveParentSet() for tag in entry.tag_set.filter(user=request.user)]
        tag_list_queries.append(entry.tag_set.filter(user=request.user))
    entry_tag_list = Tag.objects.none().union(query_tag_set, *tag_list_queries)

    entry_tag_list = sorted([t for t in entry_tag_list], key=lambda t: len(t.recursiveEntrySet()), reverse=True)

    data['entry_set']      = EntrySerializer(entry_set,    many=True, context = { 'request': request }).data
    data['entry_tag_list'] = TagSerializer(entry_tag_list, many=True, context = { 'request': request }).data
    data['tag_list']       = TagSerializer(tag_list,       many=True, context = { 'request': request }).data
    data['query']          = query_json

    return Response(data)
