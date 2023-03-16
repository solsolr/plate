from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from plate import views

app_name = 'plate'

urlpatterns = [

    path('', views.login, name='login'),  # 로그인
    path('<str:a_id>/',views.index, name='index'),  # 기본 메인
    path('det/<str:a_id>/',views.det_index, name='det_index'),  # 검출 후 메인
    path('tkflwk23/create/', views.plate_create, name='create'),  # 등록
    path('withhold/<int:c_id>/<str:a_id>', views.plate_withhold, name='plate_withhold'),  # 보류
    path('start/<str:a_id>',views.plate_start, name='start'),  # 검출

] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)