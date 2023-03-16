from django.contrib import admin

# Register your models here.
from .models import Admin,Car


class AdminAdmin(admin.ModelAdmin):
    search_fields = ['a_name']
class CarAdmin(admin.ModelAdmin):
    search_fields = ['car_num']


admin.site.register(Admin, AdminAdmin)  # Admin 클래스를 admin에 등록
admin.site.register(Car, CarAdmin)  # Car 클래스를 admin에 등록