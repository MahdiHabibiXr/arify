# Generated by Django 4.2.3 on 2023-07-10 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0015_alter_video_video'),
    ]

    operations = [
        migrations.AddField(
            model_name='exporturl',
            name='high_model',
            field=models.CharField(default='download link', max_length=500),
        ),
        migrations.AddField(
            model_name='exporturl',
            name='med_model',
            field=models.CharField(default='download link', max_length=500),
        ),
    ]
