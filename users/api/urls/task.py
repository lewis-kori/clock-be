from django.urls import path
from ..views.task import TaskListCreateAPIView

urlpatterns = [
    path('tasks/',TaskListCreateAPIView.as_view(), name='tasks'),
]
