# Generated by Django 4.2.1 on 2023-07-13 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0018_alter_nerf_apikey'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApiKey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=500)),
                ('active', models.BooleanField(default=True)),
                ('remaining', models.IntegerField()),
            ],
        ),
    ]
