from rest_framework import serializers

from .models import TodoItem


class TodoItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoItem
        fields = ('id', 'title', 'description', 'is_done', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')
