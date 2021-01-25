from rest_framework.serializers import ModelSerializer, SerializerMethodField

from ...models import Task


class TaskSerializer(ModelSerializer):
    online_servers = SerializerMethodField()
    message = SerializerMethodField()
    class Meta:
        model = Task
        fields = '__all__'

    def get_online_servers(self, obj):
        return obj.online_servers

    def get_message(self, obj):
        if obj.task != 'REPORT':
            return f'{obj.task.lower()} {obj.servers} servers.'
        return f'Report {obj.online_servers} servers running.'
