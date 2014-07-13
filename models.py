from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


class TaskTag(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=200)
    
    class Meta:
        ordering = ['category', 'title']
    
    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('tasktag_detail', kwargs={'pk': self.pk})


class Task(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_start = models.DateTimeField(blank=True, null=True)
    date_due = models.DateTimeField(blank=True, null=True)
    has_due = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    repeat = models.BooleanField(default=False)
    tags = models.ManyToManyField(TaskTag, blank=True, null=True)
    parent = models.ForeignKey('self', blank=True, null=True)

    class Meta:
        ordering = ['-has_due', 'date_due']
    
    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('task_detail', kwargs={'pk': self.pk})
