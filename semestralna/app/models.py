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
        return self.message

    def get_comments(id):
        comments = Comment.objects.raw('''WITH RECURSIVE comments AS (
            SELECT * FROM app_comment WHERE id = %s
            UNION ALL
            SELECT m.* FROM app_comment AS m JOIN comments AS t ON m.parent_id_id = t.id
            )
            SELECT * FROM comments;''', [id])
        return comments

    def delete_comment(self):
        self.message = None
        self.author = None
        self.date = None
        self.save()