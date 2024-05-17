from django.core.paginator import Paginator
from django.shortcuts import render
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
        "questions": item,
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
    return render(request, "register.html")


def login(request):
    popular_tags = Tag.objects.get_popular()
    return render(request, "login.html", {"popular_tags": popular_tags})
