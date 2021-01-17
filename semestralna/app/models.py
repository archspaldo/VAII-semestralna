from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime

# Create your models here.

class Discussion(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    author = models.ForeignKey(
        get_user_model(), null=True, on_delete=models.SET_NULL)
    date = models.DateTimeField(default=datetime.now)

    def __str__(self) -> str:
        return self.title

class Comment(models.Model):
    discussion_id = models.ForeignKey('Discussion', to_field='id', null=True, on_delete=models.CASCADE)
    parent_id = models.ForeignKey('Comment', to_field='id', null=True, blank=True, on_delete=models.SET_NULL, default=None)
    message = models.TextField(null=True)
    author = models.ForeignKey(get_user_model(), null=True, on_delete=models.SET_NULL)
    date = models.DateTimeField(default=datetime.now, null=True)

    def __str__(self) -> str:
        return (str)(self.id)

    def get_comments(self, get_self):
        r = []
        for c in Comment.objects.all().filter(parent_id=self).select_related('author'):
            r.append({ 'id' : c.id ,'parent' : c.parent_id.id, 'message' : c.message, 'author' : c.author.username, 'date' : c.date})
            _r = c.get_comments(True)
            if 0 < len(_r):
                r.extend(_r)
        return r

    def delete_comment(self):
        self.message = None
        self.author = None
        self.date = None
        self.save()