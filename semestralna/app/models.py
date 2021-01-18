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

    def get_comments_rec(self, topic):
        r = []
        for c in Comment.objects.all().filter(parent_id=self, discussion_id=topic).select_related('author'):
            r.append({ 'id' : c.id ,'parent' : c.parent_id.id, 'message' : c.message, 'author' : c.author.username, 'date' : c.date})
            _r = c.get_comments(True)
            if 0 < len(_r):
                r.extend(_r)
        return r

    def get_comments(self, topic, comment):
        _comment = Comment.objects.filter(pk = comment).first()
        _topic = Discussion.objects.filter(pk = topic).first()
        return _comment.get_comments_rec(_topic)

    def delete_comment(self):
        self.message = None
        self.author = None
        self.date = None
        self.save()

    def get_comments_all(topic):
        _topic = Discussion.objects.filter(id = topic).first()
        r = []
        if topic:
            for c in Comment.objects.filter(discussion_id = _topic).select_related('author'):
                r.append({ 'id' : c.id ,'parent' : c.parent_id.id if c.parent_id else '', 'message' : c.message, 'author' : c.author.username if c.author else '', 'date' : c.date})
        return r