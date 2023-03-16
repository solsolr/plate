from django.contrib import admin

from .models import Admin, Car  # models.py에서 모델들을 가져옴.

admin.site.register(Admin)  # Admin 클래스를 admin에 등록
admin.site.register(Car)  # Car 클래스를 admin에 등록
