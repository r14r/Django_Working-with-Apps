from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from app_auth.decorators import email_verified_required

from .forms import TodoItemForm
from .models import TodoItem


@email_verified_required
def todo_list(request):
    items = TodoItem.objects.filter(user=request.user)
    return render(request, 'app_todo/todo_list.html', {'items': items})


@email_verified_required
def todo_create(request):
    if request.method == 'POST':
        form = TodoItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.save()
            messages.success(request, 'To-do wurde erstellt.')
            return redirect('app_todo:list')
    else:
        form = TodoItemForm()

    return render(request, 'app_todo/todo_form.html', {'form': form, 'page_title': 'Neues To-do'})


@email_verified_required
def todo_update(request, pk: int):
    item = get_object_or_404(TodoItem, pk=pk, user=request.user)

    if request.method == 'POST':
        form = TodoItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'To-do wurde aktualisiert.')
            return redirect('app_todo:list')
    else:
        form = TodoItemForm(instance=item)

    return render(request, 'app_todo/todo_form.html', {'form': form, 'page_title': 'To-do bearbeiten'})


@email_verified_required
def todo_delete(request, pk: int):
    item = get_object_or_404(TodoItem, pk=pk, user=request.user)
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'To-do wurde gelöscht.')
        return redirect('app_todo:list')

    return render(request, 'app_todo/todo_confirm_delete.html', {'item': item})


@email_verified_required
def todo_toggle(request, pk: int):
    item = get_object_or_404(TodoItem, pk=pk, user=request.user)
    item.is_done = not item.is_done
    item.save(update_fields=['is_done', 'updated_at'])
    return redirect('app_todo:list')
