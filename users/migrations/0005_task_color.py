# Generated by Django 3.1.5 on 2021-01-25 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20210125_1708'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='color',
            field=models.CharField(default='#fffff', max_length=7),
        ),
    ]
