from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
    url(r'^$', views.task_index, name='task_index'),
    url(r'^tasks/$', views.task_list, name='task_list'),
    url(r'^tasks/(?P<pk>\d+)$', views.task_detail, name='task_detail'),
    url(r'^tasks/new$', views.task_create, name='task_new'),
    url(r'^tasks/edit/(?P<pk>\d+)$', views.task_update, name='task_edit'),
    url(r'^tasks/delete/(?P<pk>\d+)$', views.task_delete, name='task_delete'),
    url(r'^tags/$', views.tasktag_list, name='tasktag_list'),
    url(r'^tags/(?P<pk>\d+)$', views.tasktag_detail, name='tasktag_detail'),
    url(r'^tags/new$', views.tasktag_create, name='tasktag_new'),
    url(r'^tags/edit/(?P<pk>\d+)$', views.tasktag_update, name='tasktag_edit'),
    url(r'^tags/delete/(?P<pk>\d+)$', views.tasktag_delete, name='tasktag_delete'),
    url(r'^notes/$', views.note_list, name='note_list'),
    url(r'^notes/(?P<pk>\d+)$', views.note_detail, name='note_detail'),
    url(r'^notes/new$', views.note_create, name='note_new'),
    url(r'^notes/edit/(?P<pk>\d+)$', views.note_update, name='note_edit'),
    url(r'^notes/delete/(?P<pk>\d+)$', views.note_delete, name='note_delete'),

)
