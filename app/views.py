from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.forms import model_to_dict
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.decorators.http import require_http_methods, require_POST
from django.conf import settings

from .forms import LoginForm, RegisterForm, AskForm, SettingsForm, AnswerForm
from .models import Tag, Question, Answer, Profile, QuestionLike, AnswerLike


class HttpResponseAjax(JsonResponse):
    def __init__(self, status='ok', **kwargs):
        kwargs['status'] = status
        super().__init__(kwargs)


class HttpResponseAjaxError(HttpResponseAjax):
    def __init__(self, code, message):
        super().__init__(
            status='error', code=code, message=message
        )

def login_required_ajax(view):
    def view2(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view(request, *args, **kwargs)
        elif request.is_ajax():
            return HttpResponseAjaxError(
                code="no_auth",
                message=u'Login required',
            )

    return view2


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
    if request.method == 'POST' and request.user.is_authenticated:
        answer_form = AnswerForm(Profile.objects.get(user = request.user), data=request.POST)
        curr_answer = Answer.objects.create(
            text=answer_form.data['text'],
            creator=request.user.profile,
            question=item,
        )
        curr_answer.save()
        item.answer_count += 1
        item.save()


    ans = Answer.objects.filter(question=question_id).order_by('-created_at')
    page_obj = paginate(ans, request, 5)

    popular_tags = Tag.objects.get_popular()
    context = {
        "question": item,
        "popular_tags": popular_tags,
        "tags": Tag.objects.all(),
        "answers": page_obj
    }
    return render(request, "question.html", context)

@login_required(login_url='log_in')
def ask(request):
    print(request.GET)
    print(request.POST)
    popular_tags = Tag.objects.get_popular()

    if request.method == 'POST':
        form = AskForm(Profile.objects.get(user = request.user), data=request.POST)
        if form.is_valid():
            published_question = form.save()
            return HttpResponseRedirect(published_question.get_url())
    else:
        form = AskForm()

    return render(request, 'ask.html', {
        'form': form,
        'popular_tags': popular_tags,
        # 'best_members': best_members,
    })

def settings(request):
    user = User.objects.get(id=request.user.id)
    if request.method == 'GET':
        initial_data = model_to_dict(request.user)
        initial_data['avatar'] = request.user.profile.avatar
        user = request.user
        name = user.username
        email= user.email
        profile = Profile.objects.get(user=user)
        form = SettingsForm(initial=initial_data,
            data={
            'username': name,
            'email': email,
            'avatar': request.user.profile.avatar
            })
    elif request.method == 'POST':
        form = SettingsForm(data=request.POST, instance=request.user, files=request.FILES)
        if form.is_valid():
            print(form.cleaned_data)
            user.username = form.cleaned_data['username']
            user.email = form.cleaned_data['email']
            if form.cleaned_data['avatar']:
                profile = user.profile
                profile.avatar = form.cleaned_data['avatar']
                profile.save()
            user.save()
            form.save()
            return redirect(reverse('settings'))
    popular_tags = Tag.objects.get_popular()
    context = {
        "popular_tags": popular_tags,
        "tags": Tag.objects.all(),
        'form': form
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
                login(request, user)
                return redirect(reverse('settings'))
            else:
                user_form.add_error(field=None, error="User saving error!")
    return render(request, "register.html", {'form': user_form, "popular_tags": Tag.objects.get_popular()})

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


@login_required_ajax
@require_POST
def answer_correct(request):
    print(request.POST)
    try:
        answer_id = request.POST['id']
        answer = Answer.objects.get(id=answer_id)
        if answer.question_id.profile_id == request.user.profile:
            answer.change_mind_correct()
            answer.save()
            return HttpResponseAjax()
    except Answer.DoesNotExist:
        return HttpResponseAjaxError(code='bad_params', message='this answer is in an invalid state or does not exist')


@login_required_ajax
@require_POST
def question_vote(request):
    print(request.POST)
    if request.POST['action'] == "like":
        action = True
    else:
        action = False
    try:
        like = QuestionLike.objects.get(profile_id=request.user.profile,
                                        question_id=Question.objects.get(id=request.POST['id']))

        if like.is_like == action:
            return HttpResponseAjax(new_rating=like.delete())

        like.change_mind()
        like.save()
        return HttpResponseAjax(new_rating=Question.objects.get(id=request.POST['id']).rating)

    except QuestionLike.DoesNotExist:
        like = QuestionLike.objects.create(profile_id=request.user.profile,
                                           question_id=Question.objects.get(id=request.POST['id']),
                                           is_like=action)
        like.save()
        return HttpResponseAjax(new_rating=Question.objects.get(id=request.POST['id']).rating)
    except QuestionLike.MultipleObjectsReturned:
        return HttpResponseAjaxError(code='bad_params', message='Something is wrong with request. You can try again!')


@login_required_ajax
@require_POST
def answer_vote(request):
    print(request.POST)
    if request.POST['action'] == "like":
        action = True
    else:
        action = False
    try:
        like = AnswerLike.objects.get(profile_id=request.user.profile,
                                      answer_id=Answer.objects.get(id=request.POST['id']))

        if like.is_like == action:
            return HttpResponseAjax(new_rating=like.delete())

        like.change_mind()
        like.save()
        return HttpResponseAjax(new_rating=Answer.objects.get(id=request.POST['id']).rating)

    except AnswerLike.DoesNotExist:
        like = AnswerLike.objects.create(profile_id=request.user.profile,
                                         answer_id=Answer.objects.get(id=request.POST['id']),
                                         is_like=action)
        like.save()
        return HttpResponseAjax(new_rating=Answer.objects.get(id=request.POST['id']).rating)
    except AnswerLike.MultipleObjectsReturned:
        return HttpResponseAjaxError(code='bad_params', message='Something is wrong with request. You can try again!')