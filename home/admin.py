from django.contrib import admin
from .models import Nerf, Video, ExportTest, ExportUrl, ApiKey

# Register your models here.
admin.site.register(Nerf)
admin.site.register(Video)
admin.site.register(ExportTest)
admin.site.register(ExportUrl)
admin.site.register(ApiKey)
