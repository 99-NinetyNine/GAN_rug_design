from django.contrib import admin
from django.urls import path
from . import views

from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('send_here/', views.IndexView,name="index"),
    path("test/",views.t, name="simple_test"),
    path("test2/",views.t2, name="simple_test2"),
    path('send_fun/', views.IndexFunnyView,name="index_fun"),
    path('admin/', admin.site.urls),
    path('palette/',views.PaletteView),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
