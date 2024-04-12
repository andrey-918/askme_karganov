from django.core.paginator import Paginator
from django.shortcuts import render

# Create your views here.
QUESTIONS = [
    {
        "id": i,
        "title" : f"Question {i}",
        "text" : f"Question text number {i}",
        "photo" : "../static/images/avatar.jpg"
    } for i in range(40)
]
def index(request):
    page_num = request.GET.get('page', 1)
    paginator = Paginator(QUESTIONS, 5)
    page_obj = paginator.page(page_num)
    return render(request, "index.html", {"questions": page_obj})

def hot(request):
    return render(request, "hot.html", {"questions": QUESTIONS})

def question(request, question_id):
    item = QUESTIONS[question_id]
    return render(request, "question.html", {"question": item})