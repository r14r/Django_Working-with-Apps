from django.contrib import admin

from .models import TodoItem


@admin.register(TodoItem)
class TodoItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'is_done', 'created_at')
    list_filter = ('is_done', 'created_at')
    search_fields = ('title', 'description', 'user__username')
