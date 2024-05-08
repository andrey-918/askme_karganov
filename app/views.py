from django.core.paginator import Paginator
from django.shortcuts import render
from . import models


# Create your views here.

# TAGS = [
#     {
#         "id": i,
#         "name": f"tagName {i}",
#         "posts": [i, i + 1],
#         "questions":  [1, 2, 5, 8, 2, 12, 34, 37, 44, 71, 78, 90]
#     } for i in range(40)
# ]
# QUESTIONS = [
#     {
#         "id": i,
#         "title" : f"Question {i}",
#         "text" : f"Question text number {i}",
#         "photo" : "../static/images/avatar.jpg",
#         "tags" : [1, 2, 3],
#         "answers": [x for x in range (0, i, 2)]
#     } for i in range(400)
# ]
#
# ANSWERS = [
#     {
#         "id": i,
#         "text": f"something clever #{i}",
#         "person_id": i,
#     } for i in range (40)
# ]
#
# def paginate(objects_list, request, per_page=10):
#     page_num = request.GET.get('page', 1)
#     paginator = Paginator(objects_list, per_page)
#     try:
#         paginator.page(page_num)
#     except:
#         page_num = 1
#     return paginator.page(page_num)
#
#
#
# def index(request):
#     page_obj = paginate(QUESTIONS, request)
#     popular_tags = [TAGS[tag_id] for tag_id in range (10)]
#     return render(request, "index.html", {"questions": page_obj, "popular_tags":popular_tags, "tags": TAGS})
#
# def hot(request):
#     page_obj = paginate(QUESTIONS, request)
#     popular_tags = [TAGS[tag_id] for tag_id in range(10)]
#     return render(request, "hot.html", {"questions": page_obj, "popular_tags":popular_tags, "tags": TAGS})
#
# def question(request, question_id):
#     item = QUESTIONS[question_id]
#     popular_tags = [TAGS[tag_id] for tag_id in range(10)]
#     ans = [ANSWERS[answer_id] for answer_id in QUESTIONS[question_id]["answers"]]
#     page_obj = paginate(ans, request, 5)
#     return render(request, "question.html", {"question": item, "popular_tags":popular_tags, "tags": TAGS, "answers": page_obj})
#
# def ask(request):
#     popular_tags = [TAGS[tag_id] for tag_id in range(10)]
#     return render(request, "ask.html", {"popular_tags":popular_tags, "tags": TAGS})
#
# def settings(request):
#     popular_tags = [TAGS[tag_id] for tag_id in range(10)]
#     return render(request, "settings.html", {"popular_tags":popular_tags, "tags": TAGS})
#
# def tag_page(request, tag_id):
#     item = TAGS[tag_id]
#     popular_tags = [TAGS[tag_id] for tag_id in range(10)]
#     questions = [QUESTIONS[i] for i in item["questions"]]
#     page_obj = paginate(questions, request)
#     return render(request, "tag-page.html", {"tag": item, "popular_tags": popular_tags, "tags": TAGS, "questions": page_obj})
#
# def register(request):
#     return render(request, "register.html")
#
# def login(request):
#     popular_tags = [TAGS[tag_id] for tag_id in range(10)]
#     return render(request, "login.html", {"popular_tags": popular_tags,})


def paginate(objects_list, request, per_page=10):
    page_num = request.GET.get('page', 1)
    paginator = Paginator(objects_list, per_page)
    try:
        paginator.page(page_num)
    except:
        page_num = 1
    return paginator.page(page_num)


def index(request):
    questions = models.Question.objects.get_new()
    page_obj = paginate(questions, request)
    popular_tags = [models.Tag.objects.get(pk=tag_id) for tag_id in range(10)]
    return render(request, "index.html", {"questions": page_obj, "popular_tags": popular_tags, "tags": models.Tag.objects.get_new()})


def hot(request):
    questions = models.Question.objects.get_hot()
    page_obj = paginate(questions, request)
    popular_tags = [models.Tag.objects.get(pk=tag_id) for tag_id in range(10)]
    return render(request, "hot.html", {"questions": page_obj, "popular_tags": popular_tags, "tags": models.Tag.objects})


def question(request, question_id):
    item = models.Question.objects.get(pk=question_id)
    popular_tags = [models.Tag.objects.get(pk=tag_id) for tag_id in range(10)]
    ans = models.Answer.objects.filter(question=question_id)
    page_obj = paginate(ans, request, 5)
    return render(request, "question.html",
                  {"question": item, "popular_tags": popular_tags, "tags": models.Tag.objects, "answers": page_obj})


def ask(request):
    popular_tags = [models.Tag.objects.get(pk=tag_id) for tag_id in range(10)]
    return render(request, "ask.html", {"popular_tags": popular_tags, "tags": models.Tag.objects})


def settings(request):
    popular_tags = [models.Tag.objects.get(pk=tag_id) for tag_id in range(10)]
    return render(request, "settings.html", {"popular_tags": popular_tags, "tags": models.Tag.objects})


def tag_page(request, tag_id):
    item = models.Tag.objects.get(tag_id)
    popular_tags = [models.Tag.objects.get(pk=tag_id) for tag_id in range(10)]
    questions = [models.Question.objects.get(i) for i in item["questions"]]
    page_obj = paginate(questions, request)
    return render(request, "tag-page.html",
                  {"tag": item, "popular_tags": popular_tags, "tags": models.Tag.objects, "questions": page_obj})


def register(request):
    return render(request, "register.html")


def login(request):
    popular_tags = [models.Tag.objects.get(pk=tag_id) for tag_id in range(10)]
    return render(request, "login.html", {"popular_tags": popular_tags, })
