# Generated by Django 3.0.8 on 2020-12-06 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasket', '0003_auto_20201027_1342'),
    ]

    operations = [
        migrations.AddField(
            model_name='day',
            name='completed_tasks',
            field=models.ManyToManyField(related_name='completedTasks', to='tasket.Task'),
        ),
    ]