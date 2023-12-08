from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.IndexView,name="index"),
    path('admin/', admin.site.urls),
    path('api/', views.ApiView,name="api"),
]
