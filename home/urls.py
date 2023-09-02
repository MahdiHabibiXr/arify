from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('view/<int:nerf_id>/', views.view, name='view'),
    path('delete/<int:nerf_id>', views.delete, name='delete'),
    path('create/', views.create, name='create'),
    path('edit/<int:nerf_id>', views.edit, name='edit'),
    path('down/<int:nerf_id>', views.download_url, name='down'),
    path('addkey', views.add_key, name='addkey'),
    path('view/wall/<int:wall_id>', views.view_wall_ar, name='view_wall'),
    path('dtv', views.dtv, name='dtv')

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
