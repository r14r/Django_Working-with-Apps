from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django import forms
from django.contrib import messages
from functools import wraps

User = get_user_model()


def staff_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            from django.conf import settings
            return redirect(settings.LOGIN_URL)
        if not (request.user.is_staff or request.user.is_superuser):
            from django.core.exceptions import PermissionDenied
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return wrapper


class GroupForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Group
        fields = ['name', 'permissions']


class UserGroupForm(forms.Form):
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )


@staff_required
def user_list(request):
    users = User.objects.all().order_by('username')
    return render(request, 'app_admin/user_list.html', {'users': users})


@staff_required
def user_add(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User created successfully.')
            return redirect('app_admin:user_list')
    else:
        form = UserCreationForm()
    return render(request, 'app_admin/user_form.html', {'form': form, 'title': 'Add User'})


@staff_required
def user_change_password(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Password for {user.username} updated.')
            return redirect('app_admin:user_list')
    else:
        form = SetPasswordForm(user)
    return render(request, 'app_admin/user_form.html', {'form': form, 'title': f'Change Password: {user.username}'})


@staff_required
def group_list(request):
    groups = Group.objects.prefetch_related('permissions').all()
    return render(request, 'app_admin/group_list.html', {'groups': groups})


@staff_required
def group_add(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Group created successfully.')
            return redirect('app_admin:group_list')
    else:
        form = GroupForm()
    return render(request, 'app_admin/group_form.html', {'form': form, 'title': 'Add Group'})


@staff_required
def group_edit(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    if request.method == 'POST':
        form = GroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            messages.success(request, 'Group updated successfully.')
            return redirect('app_admin:group_list')
    else:
        form = GroupForm(instance=group)
    return render(request, 'app_admin/group_form.html', {'form': form, 'title': f'Edit Group: {group.name}'})


@staff_required
def user_assign_groups(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        form = UserGroupForm(request.POST)
        if form.is_valid():
            user.groups.set(form.cleaned_data['groups'])
            messages.success(request, f'Groups updated for {user.username}.')
            return redirect('app_admin:user_list')
    else:
        form = UserGroupForm(initial={'groups': user.groups.all()})
    return render(request, 'app_admin/user_assign_groups.html', {'form': form, 'managed_user': user})
