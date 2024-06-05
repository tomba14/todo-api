from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class TodoList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.month.strftime("%B %Y")}'

class Todo(models.Model):
    todo_list = models.ForeignKey(TodoList, related_name='todos', on_delete=models.CASCADE)
    content = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    is_daily = models.BooleanField(default=False)
    expiration_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.content