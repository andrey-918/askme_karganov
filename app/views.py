from django.shortcuts import render

# Create your views here.
QUESTIONS = [
    {
        "title" : f"Question {i}",
        "text" : f"Question text number {i}",
        "photo" : "../static/images/avatar.jpg"
    } for i in range(10)
]
def index(request):
    return render(request, "index.html", {"questions": QUESTIONS})