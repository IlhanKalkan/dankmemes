# Generated by Django 2.1.4 on 2018-12-27 00:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('memes', '0008_auto_20181227_0032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.FileField(default='media/default.jpg', upload_to=''),
        ),
    ]
