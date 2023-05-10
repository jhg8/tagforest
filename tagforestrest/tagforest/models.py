from django.db import models
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError
from django.utils.functional import classproperty

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class GroupProfile(models.Model):
    group = models.OneToOneField(Group, on_delete=models.CASCADE)

class Tree(models.Model):
    name = models.CharField(max_length=255, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    default_category = models.ForeignKey('TagCategory', on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    public = models.BooleanField(default=False)

    class Meta:
        unique_together = ('name', 'user')

    def __str__(self):
        return self.name

class TagCategory(models.Model):
    name = models.CharField(max_length=255, blank=False)
    color = models.CharField(max_length=255, blank=False, default="ffffff")
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    tree = models.ForeignKey(Tree, on_delete=models.CASCADE, blank=False)
    use_as_filter = models.BooleanField(default=True)
    show_in_results = models.BooleanField(default=True)

    class Meta:
        unique_together = ('name', 'user', 'tree')
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=255, blank=False)
    parent_set = models.ManyToManyField('self',
                                        symmetrical=False,
                                        related_name='child_set',
                                        related_query_name='child',
                                        blank=True
    )
    category = models.ForeignKey(TagCategory, on_delete=models.CASCADE, blank=False)
    score = models.FloatField(blank=False, default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    tree = models.ForeignKey(Tree, on_delete=models.CASCADE, blank=False)
    content = models.TextField(blank=True)

    class Meta:
        unique_together = ('name', 'user', 'tree')

    def __str__(self):
        return self.name

    def clean(self):
        if self.parent_set.filter(name=self.name):
            raise ValidationError("Tag cannot contain itself in parent set")

class Graph():

    def __init__(self, user, tree):
        self.user = user
        self.tree = tree
        self.update()

    def update(self):

        self.graph = {}
        self.graph_rev = {}
        self.all = set()

        for tag in Tag.objects.filter(user=self.user, tree=self.tree):
            self.graph[tag.name] = [parent.name for parent in tag.parent_set.all()]
            self.all.add(tag.name)
        for tag in self.graph:
            self.graph_rev.setdefault(tag, [])
            for parent in self.graph[tag]:
                self.graph_rev.setdefault(parent, []).append(tag)

    @classmethod
    def _BFS(cls, node_set, graph):
        visited = set()

        for node in node_set:
            if node in visited:
                continue
            if node not in graph:
                continue
            queue=[]
            visited.add(node)
            queue.append(node)

            while queue:
                s=queue.pop(0)
                
                for x in graph[s]:
                    if x not in visited:
                        visited.add(x)
                        queue.append(x)
        return visited

    def ascendantSet(self, tag_set):
        return self._BFS(tag_set, self.graph)

    def descendantSet(self, tag_set):
        return self._BFS(tag_set, self.graph_rev)

    def extendedAscendantSet(self, tag_set):
        extended_ascendant_set = self.ascendantSet(tag_set)
        descendant_set = self.descendantSet(tag_set)
        for tag in descendant_set:
            extended_ascendant_set.add(tag)
            for parent in self.graph.get(tag, []):
                extended_ascendant_set.add(parent)
        return extended_ascendant_set

    def extendedDescendantSet(self, tag_set):
        extended_descendant_set = self.ascendantSet(tag_set).union(self.descendantSet(tag_set))
        child_set = set()
        for tag in tag_set:
            for child in self.graph_rev.get(tag, []):
                child_set.add(child)
        for tag in self.ascendantSet(child_set):
            extended_descendant_set.add(tag)
        return extended_descendant_set
