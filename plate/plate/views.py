from .models import Car,Admin,Citizen
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from .forms import CarForm,AdminForm
from .car_exe import classify_number
from django.utils import timezone


def login(request):  # 로그인 페이지
  if request.method == "POST":
    id = request.POST['id']
    pw = request.POST['password']
    admin = Admin.objects.order_by('a_id')  # 관리자 데이터를 받아옴.

    for a in admin:
      if a.a_id == id and a.a_pw == pw:  # 하나라도 일치하면 로그인 성공
        return redirect('plate:index', a_id=a.a_id)  # 해당 관리자를 넘김

  form = AdminForm()
  context = {'form': form }
  return render(request, 'plate/login.html', context)  # 폼 페이지


def index(request,a_id): # 기본 페이지
  page = request.GET.get('page', '1')  # 페이지
  citizen_list = Citizen.objects.order_by('c_num')  # 시민 리스트
  car_list = Car.objects.order_by('car_num')  # 차량 리스트
  admin = Admin.objects.filter(a_id=a_id)  # 해당 관리자 로그인

  # paginator = Paginator(citizen_list,1)  # 페이지당 1개씩 보여주기
  paginator2 = Paginator(admin,1)
  paginator3 = Paginator(car_list,1)

  # page_obj = paginator.get_page(page)  # 페이지 객체
  page_obj2 = paginator2.get_page(page)
  page_obj3 = paginator3.get_page(page)

  context = {'citizen_list': citizen_list, 'admin': page_obj2, 'car_list': page_obj3 }  # 차량과 시민정보를 index에 전달
  return render(request, 'plate/index.html', context)


def plate_create(request):  # 차 등록
  form = CarForm()
  admin = Admin.objects.filter(a_id='tkflwk23')
  context = {'form': form,'admin': admin}
  return render(request, 'plate/form.html', context)  # 폼 페이지


def plate_withhold(request, c_id, a_id):  # 차 보류
  car = get_object_or_404(Car, pk=c_id)
  admin = get_object_or_404(Admin, pk=a_id)

  admin.a_wh += 1  # 보류 횟수 1증가
  admin.a_id = a_id
  car.delete()
  admin.save()
  return redirect('plate:index',a_id=a_id)  # 삭제 후, 메인 페이지로 돌아감.


def plate_start(request,a_id):  # 번호판 검출 ( 저장하기 누르면 )
  citizen_list = Citizen.objects.order_by('c_num')  # 시민 정보를 가져옴.
  car = Car()  # Car모델 객체 생성
  car.car_num = request.POST['car_num']

  citizen = None  # 시민 객체 (단속횟수 저장을 위함)

  for cit in citizen_list:
    if cit.c_num == car.car_num:  # 해당 시민의 번호판과 일치하면
      citizen = get_object_or_404(Citizen,pk=cit.id)
      break

  car.car_image = request.FILES['car_image']
  car_no = request.FILES['car_image']
  print(car_no)
  car.save()

  admin = get_object_or_404(Admin,pk=a_id)
  if classify_number.start(car_no)[1] != -1:
    admin.a_de += 1  # 검출 횟수 1 증가
    car.car_check = 1  # 검출 차량으로 분류
    citizen.c_count += 1  # 단속 횟수
    citizen.c_date = timezone.now()  # 단속 일자
    admin.save()
    citizen.save()

  if car.car_num == request.POST['car_num']:
    car.car_image = "images/r_%s"%car_no

  car.save()
  return redirect('plate:det_index',a_id=a_id)


def det_index(request,a_id):  # 검출 후 기본 페이지
  page = request.GET.get('page', '1')  # 페이지
  citizen_list = Citizen.objects.order_by('c_num')  #  번호로 정렬
  car_list = Car.objects.order_by('car_num')
  admin = Admin.objects.filter(a_id=a_id)

  paginator2 = Paginator(admin, 1)
  paginator3 = Paginator(car_list, 1)

  # page_obj = paginator.get_page(page)  # 페이지 객체
  page_obj2 = paginator2.get_page(page)
  page_obj3 = paginator3.get_page(page)

  context = {'citizen_list': citizen_list, 'admin': page_obj2, 'car_list': page_obj3}  # 차량과 시민정보를 index에 전달
  return render(request, 'plate/index.html', context)