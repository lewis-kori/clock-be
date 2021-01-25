from django.urls import path, include

urlpatterns = [
    path('v1/',include('users.api.urls.task')),
]
