# Generated by Django 3.0.8 on 2020-09-16 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0004_auto_20200916_1213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='liked_posts',
            field=models.ManyToManyField(blank=True, related_name='liked', to='network.Post'),
        ),
    ]