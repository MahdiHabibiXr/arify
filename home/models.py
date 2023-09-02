from django.db import models
from django.core.exceptions import ValidationError


class Nerf(models.Model):
    slug = models.CharField(max_length=400)
    apikey = models.CharField(max_length=500, default='')
    video_id = models.IntegerField()
    called_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
    title = models.TextField(default='New Capture')
    user_id = models.IntegerField(default=1)
    file_id = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.title} | Nerf {self.id} | Status : {self.status}'


def validate_file_extension(value):
    if not value.name.endswith('.mp4'):
        raise ValidationError(
            u'File not supported, only vide files are supported!')


class Video(models.Model):
    title = models.TextField()
    video = models.FileField(upload_to='videos/%Y/%m/%d/',
                             validators=[validate_file_extension])
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title} | video {self.id}'


class ExportTest(models.Model):
    nerf_id = models.IntegerField(default=0)
    thumb = models.ImageField(upload_to='images/%Y/%m/%d/')
    low_glb = models.FileField(upload_to='models/%Y/%m/%d/')
    med_glb = models.FileField(upload_to='models/%Y/%m/%d/')

    def __str__(self):
        return f'Nerf {self.nerf_id} files {self.id}'


class ExportUrl(models.Model):
    nerf_id = models.IntegerField()
    thumb = models.CharField(max_length=500)
    low_model = models.CharField(max_length=500)
    med_model = models.CharField(max_length=500, default='download link')
    high_model = models.CharField(max_length=500, default='download link')

    def __str__(self):
        return f'Nerf {self.nerf_id} urls {self.id}'


class ApiKey(models.Model):
    key = models.CharField(max_length=500)
    active = models.BooleanField(default=True)
    remaining = models.IntegerField()

    def __str__(self):
        return f'{self.id} : Status {self.active} | Remaining : {self.remaining}'
