from django.db import models
from django.contrib.auth.models import User, Group

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class GroupProfile(models.Model):
    group = models.OneToOneField(Group, on_delete=models.CASCADE)

class Tag(models.Model):
    name = models.CharField(max_length=255, blank=False)
    parent_set = models.ManyToManyField('self',
                                        symmetrical=False,
                                        related_name='child_set',
                                        related_query_name='child',
                                        blank=True
    )
    score = models.FloatField(blank=False, default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)

    class Meta:
        unique_together = ('name', 'user')

    def __str__(self):
        return self.name

    # TODO : Use graph algorithms instead of query unions
    def recursiveChildSet(self):
        return self.child_set.filter(user=self.user).union(*[tag.recursiveChildSet() for tag in self.child_set.all()])
    def recursiveParentSet(self):
        return self.parent_set.filter(user=self.user).union(*[tag.recursiveParentSet() for tag in self.parent_set.all()])
    def recursiveEntrySet(self):
        return Entry.objects.none().union(self.entry_set.filter(user=self.user), *[tag.entry_set.filter(user=self.user) for tag in self.recursiveChildSet()])
    
class Entry(models.Model):
    name = models.CharField(max_length=255, blank=False)
    tag_set = models.ManyToManyField(Tag)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    content = models.TextField(blank=True)

    def __str__(self):
        return self.name
    class Meta: 
        verbose_name_plural = 'entries'
