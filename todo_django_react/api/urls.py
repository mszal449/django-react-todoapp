from django.contrib import admin
from django.urls import path, include
from .views import *


urlpatterns = [
    path('tasks/', tasks, name='tasks'),
    path('tasks/<int:pk>', task, name='task_single'),
    path('tasks/create', task_create, name='task_create'),
    path('tasks/update/<int:pk>', task_update, name='task_update'),
    path('tasks/delete/<int:pk>', task_delete, name='task_delete'),
]
