from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings

from .forms import LoginForm, RegisterForm
from .models import Tag, Question, Answer, Profile


def paginate(objects_list, request, per_page=10):
    page_num = request.GET.get('page', 1)
    paginator = Paginator(objects_list, per_page)
    try:
        paginator.page(page_num)
    except:
        page_num = 1
    return paginator.page(page_num)


def index(request):
    questions = [val for val in Question.objects.get_new()]
    page_obj = paginate(questions, request)
    popular_tags = Tag.objects.get_popular()
    context = {
        "questions": page_obj,
        "popular_tags": popular_tags,
        "tags": Tag.objects.all()
    }
    return render(request, "index.html", context)


def hot(request):
    questions = Question.objects.get_hot()
    page_obj = paginate(questions, request)
    popular_tags = Tag.objects.get_popular()
    context = {
        "questions": page_obj,
        "popular_tags": popular_tags,
        "tags": Tag.objects.all()
    }
    return render(request, "hot.html", context)


def question(request, question_id):
    item = Question.objects.get(pk=question_id)
    ans = Answer.objects.filter(question=question_id)
    page_obj = paginate(ans, request, 5)
    popular_tags = Tag.objects.get_popular()
    context = {
        "question": item,
        "popular_tags": popular_tags,
        "tags": Tag.objects.all(),
        "answers": page_obj
    }
    return render(request, "question.html", context)


def ask(request):
    popular_tags = Tag.objects.get_popular()
    context = {
        "popular_tags": popular_tags,
        "tags": Tag.objects.all(),
    }
    return render(request, "ask.html", context)


def settings(request):
    popular_tags = Tag.objects.get_popular()
    context = {
        "popular_tags": popular_tags,
        "tags": Tag.objects.all(),
    }
    return render(request, "settings.html", context)

def tag_page(request, tag_id):
    item = Tag.objects.get(pk=tag_id)
    popular_tags = Tag.objects.get_popular()
    questions = [question for question in Question.objects.get_by_tag(tag=tag_id)]
    page_obj = paginate(questions, request)
    context = {
        "tag": item,
        "popular_tags": popular_tags,
        "tags": Tag.objects.all(),
        "questions": page_obj
    }
    return render(request, "tag-page.html", context)

def register(request):
    if request.method == 'GET':
        user_form = RegisterForm()
    if request.method == 'POST':
        user_form = RegisterForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            if user:
                return redirect(reverse('index'))
            else:
                user_form.add_error(field=None, error="User saving error!")
    return render(request, "register.html", {'form': user_form})



def logout(request):
    auth.logout(request)
    return redirect(reverse('log_in'))

def log_in(request):
    if request.method == 'GET':
        login_form = LoginForm()
    if request.method == 'POST':
        login_form = LoginForm(data=request.POST)
        if login_form.is_valid():
            user = authenticate(request, **login_form.cleaned_data)
            if user:
                login(request, user)
                return redirect(reverse('index'))
        print('Failed to login')
    return render(request, "login.html", context={"form": login_form, "popular_tags":Tag.objects.get_popular()})