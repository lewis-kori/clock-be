from collections import defaultdict
from random import choice, randrange

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST)
from rest_framework.views import APIView

from ...models import Task
from ..serializers.task import TaskSerializer


class TaskListCreateAPIView(APIView):
    permission_classes = [
        AllowAny,
    ]

    def post(self, request, *args, **kwargs):
        data = request.data
        colors = [
            '#636363', '#a2ab58', '#C6FFDD', '#f7797d', '#FBD786', '#b91d73',
            '#1a2a6c', '#fdbb2d', '#200122', '#614385'
        ]

        if data['task'] == 'START':
            server_count = randrange(10, 21)
            task = Task.objects.create(servers=server_count,
                                       task=data['task'],
                                       time=data['time'],
                                       actual_time=data['actual_time'],
                                       color=choice(colors),
                                       priority=1)
            serializer = TaskSerializer(task)
            return Response(serializer.data, status=HTTP_201_CREATED)

        elif data['task'] == 'STOP':
            # Check if there's a start task slotted in
            tasks = Task.objects.filter(task='START')

            # if tasks exists exit without creating record
            if tasks.exists():
                latest_start_task = Task.objects.filter(task='START').first()
                server_count = randrange(5,
                                         latest_start_task.online_servers + 1)
                task = Task.objects.create(servers=server_count,
                                           task=data['task'],
                                           time=data['time'],
                                           actual_time=data['actual_time'],
                                           color=choice(colors),
                                           priority=2)
                serializer = TaskSerializer(task)
                return Response(serializer.data, status=HTTP_201_CREATED)

        elif data['task'] == 'REPORT':
            latest_start_task = Task.objects.filter(task='START').first()
            task = Task.objects.create(task=data['task'],
                                       time=data['time'],
                                       actual_time=data['actual_time'],
                                       servers=latest_start_task.online_servers,
                                       color=choice(colors),
                                       priority=3)
            serializer = TaskSerializer(task)
            return Response(serializer.data, status=HTTP_201_CREATED)

        return Response(status=HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        times = Task.objects.all().values('time')
        # remove duplicates and sort
        unique_times = sorted(set([time['time'] for time in times]))
        time_dict = defaultdict(list)
        for time in unique_times:
            time_tasks = Task.objects.filter(time=time)
            for task in time_tasks:

                time_task_object = {
                    'task': task.task,
                    'actual_time': task.actual_time,
                    'priority': task.priority,
                    'id': task.id,
                    'message': task.message,
                }
                time_dict[f'{time}'].append(time_task_object)
                time_dict[f'{time}'].sort(key=self.take_priority)
        return Response(time_dict, status=HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        # clear all data use on page refresh (frontend)
        Task.objects.all().delete()
        return Response(status=HTTP_204_NO_CONTENT)

    # sort by priority
    def take_priority(self, element):
        return element['priority']

