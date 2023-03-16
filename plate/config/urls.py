"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from pybo import views
from pybo.views import base_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pybo/', include('pybo.urls')),
    path('common/', include('common.urls')),
    path('plate/', include('plate.urls')),
    path('', base_views.index, name='index'),    # '/' 에 해당되는 path
]
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)  # 이미지 url 경로 설정
# 불러올 때는 plate와 동등한 위치인 media에서 불러오므로 프로젝트 경로에서 불러와야 한다.
