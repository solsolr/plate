from django import forms
from .models import Car,Admin


class CarForm(forms.ModelForm):
    class Meta:
        model = Car  # 사용할 모델
        fields = ['car_num', 'car_image']  # CarForm에서 사용할 Car 모델의 속성


class AdminForm(forms.ModelForm):
    class Meta:
        model = Admin
        fields = {'a_de','a_wh'}  # AdminForm에서 사용할 Admin 모델의 속성
