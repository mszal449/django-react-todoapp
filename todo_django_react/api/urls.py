from django.urls import path
from . import views


urlpatterns = [
    path('tasks/', views.tasks, name='tasks'),
    path('tasks/<int:pk>', views.task, name='task_single'),
    path('tasks/create', views.task_create, name='task_create'),
    path('tasks/update/<int:pk>', views.task_update, name='task_update'),
    path('tasks/delete/<int:pk>', views.task_delete, name='task_delete'),
]
