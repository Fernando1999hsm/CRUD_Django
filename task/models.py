from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    date_completed = models.DateTimeField(null=True, blank=True)
    date_created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    priority = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.title + ' - by ' + self.user.username