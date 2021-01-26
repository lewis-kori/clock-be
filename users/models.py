from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

TASK_CHOICES = (
    ('START','START'),
    ('STOP','STOP'),
    ('REPORT','REPORT'),
)

class CommonInfo(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

# define our own custom methods for user model management
class CustomUserManager(UserManager):
    def create_user(self,
                    username=None,
                    email=None,
                    password=None,
                    **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, email, password, **extra_fields)

    def create_superuser(self,
                         username=None,
                         email=None,
                         password=None,
                         **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, email, password, **extra_fields)

# define our custom user model
class UserAccount(AbstractUser):
    objects = CustomUserManager()

    def __str__(self) -> str:
        return self.get_full_name()


class Task(CommonInfo):
    task = models.CharField(max_length=30, choices=TASK_CHOICES, default='START')
    servers = models.PositiveIntegerField(null=True, blank=True) # reports don't need this value
    time = models.TimeField() # time on frontend clock
    actual_time = models.TimeField() 
    color = models.CharField(max_length=7, default='#fffff')
    priority =models.PositiveSmallIntegerField(default=1)

    def __str__(self) -> str:
        return self.task

    @property
    def online_servers(self) -> int:
        start_tasks = Task.objects.filter(task='START')
        stop_tasks = Task.objects.filter(task='STOP')

        if stop_tasks.exists() and start_tasks.exists():
            started_servers = [server['servers'] for server in start_tasks.values('servers')]
            stopped_servers = [server['servers'] for server in stop_tasks.values('servers')]

            started_servers_count = sum(started_servers)
            stopped_servers_count = sum(stopped_servers)
            return started_servers_count - stopped_servers_count
        elif start_tasks.exists():
            started_servers = [server['servers'] for server in start_tasks.values('servers')]
            return sum(started_servers)
        return 0

    @property
    def message(self):
        if self.task != 'REPORT':
            return f'{self.task.lower()} {self.servers} servers.'
        return f'Report {self.online_servers} servers running.'