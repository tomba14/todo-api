from rest_framework import serializers
from .models import TodoList, Todo

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ['id', 'content', 'description', 'is_completed', 'is_daily', 'expiration_date']
        read_only_fields = ['todo_list']  # make lists only readable because we are setting this in the perform create

class TodoListSerializer(serializers.ModelSerializer):
    todos = TodoSerializer(many=True, read_only=True)

    class Meta:
        model = TodoList
        fields = ['id', 'created_at', 'todos']