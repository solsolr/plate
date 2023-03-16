from ..models import Question
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

def index(request):
    # return HttpResponse("안녕하세요 pybo 어플리케이션에 오신 것을 환영합니다.")
    page = request.GET.get('page', '1')     # 페이지
    question_list = Question.objects.order_by('-create_date')
    paginator = Paginator(question_list, 10)    # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {'question_list': page_obj}
    return render(request, 'pybo/question_list.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)