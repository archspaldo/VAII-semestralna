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

    def __str__(self):
        return self.title
