from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from plate import views

app_name = 'plate'

urlpatterns = [
    path('',views.index,name='index'),
    path('create/', views.plate_create, name='plate_create'),
    path('withhold/<int:car_id>/<str:a_id>', views.plate_withhold,name='plate_withhold'),
    path('start/',views.plate_start,name='start')
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)