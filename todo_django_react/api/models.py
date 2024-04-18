from django.db import models


# Task model
class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    done = models.BooleanField(default=False)
    fav = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

