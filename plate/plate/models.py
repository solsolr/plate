0from django.db import models


class Admin(models.Model):  # 관리자
    a_name = models.CharField('관리자', max_length=15)  # 글자수 제한 있는 varchar 자료형
    a_id = models.CharField('아이디', max_length=15, primary_key=True)  # 기본 키
    a_pw = models.CharField('비밀번호', max_length=15)
    a_de = models.IntegerField('검출한 수', default=0)
    a_wh = models.IntegerField('보류한 수',default=0)

    class Meta:
        db_table = 'Admin'  # 테이블 명


class Car(models.Model):  # 차
    car_num = models.CharField('번호판', max_length=15, unique=True)  # 차 번호는 유일하다.
    car_image = models.ImageField(upload_to="images/",unique=True)
    class Meta:
        db_table = 'Car'  # 테이블 명


class Citizen(models.Model):  # 시민
    car = models.ForeignKey(Car, on_delete=models.CASCADE)  # 시민은 여러 개의 차를 가질 수 있다.
    c_name = models.CharField('차주', max_length=15)
    c_count = models.IntegerField("단속횟수", default=0)
    c_tel = models.CharField('연락처', max_length=15, primary_key=True)  # 기본 키
    c_addr = models.TextField('거주지')
    c_date = models.DateTimeField('단속일자', null=True, blank=True)  # 단속이 아닐 시 null

    class Meta:
        db_table = 'Citizen'  # 테이블 명

