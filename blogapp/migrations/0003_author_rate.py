# Generated by Django 3.1.7 on 2021-03-25 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0002_post_read'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='rate',
            field=models.IntegerField(default=0),
        ),
    ]
