# Generated by Django 4.2.1 on 2023-07-06 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0013_remove_video_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='nerf',
            name='file_id',
            field=models.IntegerField(default=0),
        ),
    ]
