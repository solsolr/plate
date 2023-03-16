from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from . import views


app_name = 'plate'

urlpatterns = [
    # base_views.py
    path('', views.index, name='index2'),
    path('<int:car_id>/', views.detail, name='detail2'),

] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)