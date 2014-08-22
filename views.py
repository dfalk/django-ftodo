from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotFound
from django.forms import ModelForm
from django.contrib.auth.decorators import login_required
from datetime import datetime, date, timedelta

from .models import Task, TaskTag, Note


class TaskForm(ModelForm):

    def __init__(self, *args, **kwargs):
        current_user = kwargs.pop('user')
        # Then, let the ModelForm initialize:
        super(TaskForm, self).__init__(*args, **kwargs)
        # Finally, access the fields dict that was created by the super().__init__ call
        self.fields['tags'].queryset = TaskTag.objects.filter(user=current_user)

    class Meta:
        model = Task
        exclude = ['user','has_due']

class TaskTagForm(ModelForm):
    class Meta:
        model = TaskTag
        exclude = ['user']

class NoteForm(ModelForm):
    class Meta:
        model = Note
        exclude = ['user']


def task_index(request, template_name='ftodo/task_index.html'):
    tasks = []
    old_tasks = []
    bookmarks = []
    tasktags = []
    if request.user.is_authenticated():
        tasks = Task.objects.filter(user=request.user).exclude(date_due__isnull=True).filter(date_due__gte=date.today())
        old_tasks = Task.objects.filter(user=request.user).exclude(date_due__isnull=True).filter(date_due__lt=date.today()).filter(completed=False)
        bookmarks = Task.objects.filter(user=request.user).filter(bookmark=True)
        tasktags = TaskTag.objects.filter(user=request.user)
    return render(request, template_name,
        {'object_list':tasks,
        'old_list':old_tasks,
        'bookmarks':bookmarks,
        'tag_list':tasktags})
        
@login_required
def task_list(request, template_name='ftodo/task_list.html'):
    tasks = Task.objects.filter(user=request.user)
    return render(request, template_name, {'object_list':tasks})

@login_required
def goal_list(request, template_name='ftodo/goal_list.html'):
    goals = Task.objects.filter(user=request.user).filter(goal=True)
    return render(request, template_name, {'object_list':goals})

@login_required
def project_list(request, template_name='ftodo/project_list.html'):
    projects = Task.objects.filter(user=request.user).filter(project=True).order_by('parent__id')
    return render(request, template_name, {'object_list':projects})

@login_required
def task_detail(request, pk, template_name='ftodo/task_detail.html'):
    task = None
    task_result = get_object_or_404(Task, pk=pk)
    if task_result.user == request.user:
        task = task_result
        subtasks = Task.objects.filter(parent=task)
    else:
        return HttpResponseNotFound('<h1>Page not found</h1>')
    return render(request, template_name, {'object':task, 'subtasks':subtasks})

@login_required
def task_create(request, template_name='ftodo/task_form.html'):
    tasktag_id = None
    task_id = None
    task_parent = None
    if 'tag' in request.GET:
        tasktag_id = request.GET['tag']
    if 'task' in request.GET:
        task_id = request.GET['task']
        try:
            task_parent = Task.objects.get(id=task_id)
            if task_parent.user != request.user:
                task_id = None
        except Task.DoesNotExist:
            task_id = None
    form = TaskForm(
        request.POST or None,
        user=request.user,
        initial={'tags': [tasktag_id], 'parent':task_id}
    )
    if form.is_valid():
        task = form.save(commit=False)
        task.user = request.user
        if task_parent: task.parent = task_parent
        if task.date_due: task.has_due = True
        task.save()
        form.save_m2m()
        if 'next' in request.GET:
            return redirect(request.GET['next'])
        return redirect('task_index')
    return render(request, template_name, {'form':form})

@login_required
def task_update(request, pk, template_name='ftodo/task_form.html'):
    task = None
    task_result = get_object_or_404(Task, pk=pk)
    if task_result.user == request.user:
        task = task_result
    else:
        return HttpResponseNotFound('<h1>Page not found</h1>')
    form = TaskForm(request.POST or None, instance=task, user=request.user)
    if form.is_valid():
        task = form.save(commit=False)
        if task.date_due:
            task.has_due = True
        else:
            task.has_due = False
        if task.completed and task.repeat:
            task.date_due = datetime.now() + timedelta(days=1)
            task.completed = False
            task.content = task.content + "\nlog:" + str(datetime.now())
        task.save()
        form.save_m2m()
        if 'next' in request.GET:
            return redirect(request.GET['next'])
        return redirect('task_index')
    return render(request, template_name, {'object':task, 'form':form})

@login_required
def task_delete(request, pk, template_name='ftodo/task_delete.html'):
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
def tasktag_list(request, template_name='ftodo/tasktag_list.html'):
    tasktags = TaskTag.objects.filter(user=request.user)
    return render(request, template_name, {'object_list':tasktags})

@login_required
def tasktag_detail(request, pk, template_name='ftodo/tasktag_detail.html'):
    tasktag = None
    tasktag_result = get_object_or_404(TaskTag, pk=pk)
    if tasktag_result.user == request.user:
        tasktag = tasktag_result
        task_list = Task.objects.filter(user=request.user).filter(tags__in=[tasktag])
    else:
        return HttpResponseNotFound('<h1>Page not found</h1>')
    return render(request, template_name, {'object':tasktag, 'object_list':task_list})

@login_required
def tasktag_create(request, template_name='ftodo/tasktag_form.html'):
    form = TaskTagForm(request.POST or None)
    if form.is_valid():
        tasktag = form.save(commit=False)
        tasktag.user = request.user
        tasktag.save()
        return redirect('tasktag_list')
    return render(request, template_name, {'form':form})

@login_required
def tasktag_update(request, pk, template_name='ftodo/tasktag_form.html'):
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
def tasktag_delete(request, pk, template_name='ftodo/tasktag_delete.html'):
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


@login_required
def note_list(request, template_name='ftodo/note_list.html'):
    notes = Note.objects.filter(user=request.user)
    return render(request, template_name, {'object_list':notes})

@login_required
def note_detail(request, pk, template_name='ftodo/note_detail.html'):
    note = None
    note_result = get_object_or_404(Note, pk=pk)
    if note_result.user == request.user:
        note = note_result
    else:
        return HttpResponseNotFound('<h1>Page not found</h1>')
    return render(request, template_name, {'object':note})

@login_required
def note_create(request, template_name='ftodo/note_form.html'):
    note_id = None
    form = NoteForm(request.POST or None)
    if form.is_valid():
        note = form.save(commit=False)
        note.user = request.user
        note.save()
        if 'next' in request.GET:
            return redirect(request.GET['next'])
        return redirect('note_list')
    return render(request, template_name, {'form':form})

@login_required
def note_update(request, pk, template_name='ftodo/note_form.html'):
    note = None
    note_result = get_object_or_404(Note, pk=pk)
    if note_result.user == request.user:
        note = note_result
    else:
        return HttpResponseNotFound('<h1>Page not found</h1>')
    form = NoteForm(request.POST or None, instance=note)
    if form.is_valid():
        note = form.save(commit=False)
        note.save()
        if 'next' in request.GET:
            return redirect(request.GET['next'])
        return redirect('note_list')
    return render(request, template_name, {'object':note, 'form':form})

@login_required
def note_delete(request, pk, template_name='ftodo/note_delete.html'):
    note = None
    note_result = get_object_or_404(Note, pk=pk)
    if note_result.user == request.user:
        note = note_result
    else:
        return HttpResponseNotFound('<h1>Page not found</h1>')
    if request.method=='POST':
        note.delete()
        if 'next' in request.GET:
            return redirect(request.GET['next'])
        return redirect('note_list')
    return render(request, template_name, {'object':note})
