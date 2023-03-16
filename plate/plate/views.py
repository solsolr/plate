from .models import Car,Admin
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404,redirect
from .forms import CarForm
from .car_exe import classify_number

# Create your views here.


def index(request): # 기본 페이지
  page = request.GET.get('page', '1')  # 페이지
  car_list = Car.objects.order_by('car_num')
  admin = Admin.objects.filter(a_id='tkflwk23')
  paginator = Paginator(car_list,1)  # 페이지당 1개씩 보여주기
  paginator2 = Paginator(admin,1)
  page_obj = paginator.get_page(page)
  page_obj2 = paginator2.get_page(page)

  context = {'car_list': page_obj, 'admin' : page_obj2}
  return render(request, 'plate/index.html', context)


def plate_create(request):  # 차 등록
  if request.method == 'POST':  #  저장하기 눌렀을 때
    car = Car()  #  Car모델 객체 생성
    car.car_num = request.POST['car_num']  # 차 번호
    car.car_image = request.FILES['car_image']  # 차 이미지
    car_no = request.FILES['car_image']

    car.save()  # 차 저장
    return redirect('plate:index')  # 메인 페이지(정보를 그대로 전송)

  else:  # a 태그에서 이동한 Get 방식
    form = CarForm()
  context = {'form': form}
  return render(request, 'plate/form.html', context)  # 폼 페이지


def plate_withhold(request, car_id, a_id):  # 차 보류
  car = get_object_or_404(Car, pk=car_id)
  admin = get_object_or_404(Admin, pk=a_id)
  admin.a_wh += 1  # 보류 횟수 1증가
  admin.a_id = a_id
  car.delete()
  admin.save()
  return redirect('plate:index')  # 삭제 후, 메인페이지로 돌아감.

def plate_start(request):
  car = Car()  # Car모델 객체 생성
  car.car_num = request.POST['car_num']
  car.car_image = request.FILES['car_image']
  car.save()
  car_no = request.FILES['car_image']
  print(car_no)

  classify_number.start(car_no)
  if car.car_num == request.POST['car_num']:
    car.car_image = "images/r_%s" %car_no
    car.save()
  return redirect('plate:index')