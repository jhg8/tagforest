from django.db import models
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError

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
    content = models.TextField(blank=True)

    class Meta:
        unique_together = ('name', 'user')

    def __str__(self):
        return self.name

    def clean(self):
      if self.parent_set.filter(name=self.name):
        raise ValidationError("Tag cannot contain itself in parent set")

    # TODO : Use graph algorithms instead of query unions
    def recursiveChildSet(self):
        return self.child_set.filter(user=self.user).union(*[tag.recursiveChildSet() for tag in self.child_set.all()])
    def recursiveParentSet(self):
        return self.parent_set.filter(user=self.user).union(*[tag.recursiveParentSet() for tag in self.parent_set.all()])
