# Generated by Django 2.1.4 on 2018-12-26 18:44

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('memes', '0003_auto_20181226_1942'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='uploadDate',
        ),
        migrations.AddField(
            model_name='post',
            name='pub_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='date published'),
            preserve_default=False,
        ),
    ]
