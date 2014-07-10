from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
    url(r'^$', views.task_list, name='task_list'),
    url(r'^(?P<pk>\d+)$', views.task_detail, name='task_detail'),
    url(r'^new$', views.task_create, name='task_new'),
    url(r'^edit/(?P<pk>\d+)$', views.task_update, name='task_edit'),
    url(r'^delete/(?P<pk>\d+)$', views.task_delete, name='task_delete'),
    url(r'^tag/$', views.tasktag_list, name='tasktag_list'),
    url(r'^tag/(?P<pk>\d+)$', views.tasktag_detail, name='tasktag_detail'),
    url(r'^tag/new$', views.tasktag_create, name='tasktag_new'),
    url(r'^tag/edit/(?P<pk>\d+)$', views.tasktag_update, name='tasktag_edit'),
    url(r'^tag/delete/(?P<pk>\d+)$', views.tasktag_delete, name='tasktag_delete'),
)