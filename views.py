from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotFound
from django.forms import ModelForm
from django.contrib.auth.decorators import login_required
from datetime import datetime, date

from .models import Task, TaskTag

class TaskForm(ModelForm):

    def __init__(self, *args, **kwargs):
        current_user = kwargs.pop('user')
        # Then, let the ModelForm initialize:
        super(TaskForm, self).__init__(*args, **kwargs)
        # Finally, access the fields dict that was created by the super().__init__ call
        self.fields['tags'].queryset = TaskTag.objects.filter(user=current_user)

    class Meta:
        model = Task
        exclude = ['user','parent']
        
class TaskTagForm(ModelForm):
    class Meta:
        model = TaskTag
        exclude = ['user']

def task_index(request, template_name='task_index.html'):
    tasks = []
    tasktags = []
    if request.user.is_authenticated():
        tasks = Task.objects.filter(user=request.user).exclude(date_due__isnull=True).filter(date_due__gte=date.today())
        tasktags = TaskTag.objects.filter(user=request.user)
    return render(request, template_name, {'object_list':tasks, 'tag_list':tasktags})
        
@login_required
def task_list(request, template_name='task_list.html'):
    tasks = Task.objects.filter(user=request.user)
    return render(request, template_name, {'object_list':tasks})

@login_required
def task_detail(request, pk, template_name='task_detail.html'):
    task = None
    task_result = get_object_or_404(Task, pk=pk)
    if task_result.user == request.user:
        task = task_result
    else:
        return HttpResponseNotFound('<h1>Page not found</h1>')
    if task_result.user == request.user:
         task = task_result
    return render(request, template_name, {'object':task})

@login_required
def task_create(request, template_name='task_form.html'):
    form = TaskForm(request.POST or None, user=request.user)
    if form.is_valid():
        task = form.save(commit=False)
        task.user = request.user
        task.save()
        form.save_m2m()
        if 'next' in request.GET:
            return redirect(request.GET['next'])
        return redirect('task_index')
    return render(request, template_name, {'form':form})

@login_required
def task_update(request, pk, template_name='task_form.html'):
    task = None
    task_result = get_object_or_404(Task, pk=pk)
    if task_result.user == request.user:
        task = task_result
    else:
        return HttpResponseNotFound('<h1>Page not found</h1>')
    form = TaskForm(request.POST or None, instance=task, user=request.user)
    if form.is_valid():
        form.save()
        if 'next' in request.GET:
            return redirect(request.GET['next'])
        return redirect('task_index')
    return render(request, template_name, {'object':task, 'form':form})

@login_required
def task_delete(request, pk, template_name='task_delete.html'):
    task = None
    task_result = get_object_or_404(Task, pk=pk)
    if task_result.user == request.user:
        task = task_result
    else:
        return HttpResponseNotFound('<h1>Page not found</h1>')
    if request.method=='POST':
        task.delete()
        if 'next' in request.GET:
            return redirect(request.GET['next'])
        return redirect('task_index')
    return render(request, template_name, {'object':task})


@login_required
def tasktag_list(request, template_name='tasktag_list.html'):
    tasktags = TaskTag.objects.filter(user=request.user)
    return render(request, template_name, {'object_list':tasktags})

@login_required
def tasktag_detail(request, pk, template_name='tasktag_detail.html'):
    tasktag = None
    tasktag_result = get_object_or_404(TaskTag, pk=pk)
    if tasktag_result.user == request.user:
        tasktag = tasktag_result
        task_list = Task.objects.filter(user=request.user).filter(tags__in=[tasktag])
    else:
        return HttpResponseNotFound('<h1>Page not found</h1>')
    return render(request, template_name, {'object':tasktag, 'object_list':task_list})

@login_required
def tasktag_create(request, template_name='tasktag_form.html'):
    form = TaskTagForm(request.POST or None)
    if form.is_valid():
        tasktag = form.save(commit=False)
        tasktag.user = request.user
        tasktag.save()
        return redirect('tasktag_list')
    return render(request, template_name, {'form':form})

@login_required
def tasktag_update(request, pk, template_name='tasktag_form.html'):
    tasktag = None
    tasktag_result = get_object_or_404(TaskTag, pk=pk)
    if tasktag_result.user == request.user:
        tasktag = tasktag_result
    else:
        return HttpResponseNotFound('<h1>Page not found</h1>')
    form = TaskTagForm(request.POST or None, instance=tasktag)
    if form.is_valid():
        form.save()
        return redirect('tasktag_list')
    return render(request, template_name, {'object':tasktag, 'form':form})

@login_required
def tasktag_delete(request, pk, template_name='tasktag_delete.html'):
    tasktag = None
    tasktag_result = get_object_or_404(TaskTag, pk=pk)
    if tasktag_result.user == request.user:
        tasktag = tasktag_result
    else:
        return HttpResponseNotFound('<h1>Page not found</h1>')
    if request.method=='POST':
        tasktag.delete()
        return redirect('tasktag_list')
    return render(request, template_name, {'object':tasktag})
