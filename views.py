from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm
from django.contrib.auth.decorators import login_required

from .models import Task, TaskTag

class TaskForm(ModelForm):
    class Meta:
        model = Task
        
class TaskTagForm(ModelForm):
    class Meta:
        model = TaskTag

def task_index(request, template_name='task_index.html'):
    return render(request, template_name)
        
@login_required
def task_list(request, template_name='task_list.html'):
    tasks = Task.objects.all()
    return render(request, template_name, {'object_list':tasks})

@login_required
def task_detail(request, pk, template_name='task_detail.html'):
    task = get_object_or_404(Task, pk=pk)
    return render(request, template_name, {'object':task})

@login_required
def task_create(request, template_name='task_form.html'):
    form = TaskForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('task_list')
    return render(request, template_name, {'form':form})

@login_required
def task_update(request, pk, template_name='task_form.html'):
    task = get_object_or_404(Task, pk=pk)
    form = TaskForm(request.POST or None, instance=task)
    if form.is_valid():
        form.save()
        return redirect('task_list')
    return render(request, template_name, {'object':task, 'form':form})

@login_required
def task_delete(request, pk, template_name='task_delete.html'):
    task = get_object_or_404(Task, pk=pk)    
    if request.method=='POST':
        task.delete()
        return redirect('task_list')
    return render(request, template_name, {'object':task})


@login_required
def tasktag_list(request, template_name='tasktag_list.html'):
    tasktags = TaskTag.objects.all()
    return render(request, template_name, {'object_list':tasktags})

@login_required
def tasktag_detail(request, pk, template_name='tasktag_detail.html'):
    tasktag = get_object_or_404(TaskTag, pk=pk)
    return render(request, template_name, {'object':tasktag})

@login_required
def tasktag_create(request, template_name='tasktag_form.html'):
    form = TaskTagForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('tasktag_list')
    return render(request, template_name, {'form':form})

@login_required
def tasktag_update(request, pk, template_name='tasktag_form.html'):
    tasktag = get_object_or_404(TaskTag, pk=pk)
    form = TaskTagForm(request.POST or None, instance=tasktag)
    if form.is_valid():
        form.save()
        return redirect('tasktag_list')
    return render(request, template_name, {'object':tasktag, 'form':form})

@login_required
def tasktag_delete(request, pk, template_name='tasktag_delete.html'):
    tasktag = get_object_or_404(TaskTag, pk=pk)    
    if request.method=='POST':
        tasktag.delete()
        return redirect('tasktag_list')
    return render(request, template_name, {'object':tasktag})