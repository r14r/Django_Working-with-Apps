from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import TodoItemForm
from .models import TodoItem


@login_required
def todo_list(request):
    items = TodoItem.objects.filter(user=request.user)
    return render(request, 'todo/todo_list.html', {'items': items})


@login_required
def todo_create(request):
    if request.method == 'POST':
        form = TodoItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.save()
            messages.success(request, 'To-do wurde erstellt.')
            return redirect('todo:list')
    else:
        form = TodoItemForm()

    return render(request, 'todo/todo_form.html', {'form': form, 'page_title': 'Neues To-do'})


@login_required
def todo_update(request, pk: int):
    item = get_object_or_404(TodoItem, pk=pk, user=request.user)

    if request.method == 'POST':
        form = TodoItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'To-do wurde aktualisiert.')
            return redirect('todo:list')
    else:
        form = TodoItemForm(instance=item)

    return render(request, 'todo/todo_form.html', {'form': form, 'page_title': 'To-do bearbeiten'})


@login_required
def todo_delete(request, pk: int):
    item = get_object_or_404(TodoItem, pk=pk, user=request.user)
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'To-do wurde gelöscht.')
        return redirect('todo:list')

    return render(request, 'todo/todo_confirm_delete.html', {'item': item})


@login_required
def todo_toggle(request, pk: int):
    item = get_object_or_404(TodoItem, pk=pk, user=request.user)
    item.is_done = not item.is_done
    item.save(update_fields=['is_done', 'updated_at'])
    return redirect('todo:list')
