# Generated by Django 3.0.8 on 2020-09-16 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0003_user_liked_posts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
