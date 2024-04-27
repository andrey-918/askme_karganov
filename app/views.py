from django.core.paginator import Paginator
from django.shortcuts import render

# Create your views here.

TAGS = [
    {
        "id": i,
        "name": f"tagName {i}",
        "posts": [i, i + 1],
        "questions":  [1, 2, 5]
    } for i in range(40)
]
QUESTIONS = [
    {
        "id": i,
        "title" : f"Question {i}",
        "text" : f"Question text number {i}",
        "photo" : "../static/images/avatar.jpg",
        "tags" : [1, 2, 3]
    } for i in range(400)
]



def index(request):
    page_num = request.GET.get('page', 1)
    paginator = Paginator(QUESTIONS, 5)
    page_obj = paginator.page(page_num)
    popular_tags = [TAGS[tag_id] for tag_id in range (10)]
    return render(request, "index.html", {"questions": page_obj, "popular_tags":popular_tags, "tags": TAGS})

def hot(request):
    page_num = request.GET.get('page', 1)
    paginator = Paginator(QUESTIONS, 5)
    page_obj = paginator.page(page_num)
    popular_tags = [TAGS[tag_id] for tag_id in range(10)]
    return render(request, "hot.html", {"questions": page_obj, "popular_tags":popular_tags, "tags": TAGS})

def question(request, question_id):
    item = QUESTIONS[question_id]
    popular_tags = [TAGS[tag_id] for tag_id in range(10)]
    tags = [TAGS[tag_id] for tag_id in item["tags"]]
    return render(request, "question.html", {"question": item, "popular_tags":popular_tags, "tags": TAGS})

def ask(request):
    popular_tags = [TAGS[tag_id] for tag_id in range(10)]
    return render(request, "ask.html", {"popular_tags":popular_tags, "tags": TAGS})

def settings(request):
    popular_tags = [TAGS[tag_id] for tag_id in range(10)]
    return render(request, "settings.html", {"popular_tags":popular_tags, "tags": TAGS})

def tag_page(request, tag_id):
    item = TAGS[tag_id]
    popular_tags = [TAGS[tag_id] for tag_id in range(10)]
    questions = [QUESTIONS[i] for i in item["questions"]]
    return render(request, "tag-page.html", {"tag": item, "popular_tags": popular_tags, "tags": TAGS, "questions": questions})

def register(request):
    return render(request, "register.html")

def login(request):
    popular_tags = [TAGS[tag_id] for tag_id in range(10)]
    return render(request, "login.html", {"popular_tags": popular_tags,})