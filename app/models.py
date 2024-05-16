from django.db import models
from django.db.models import Count
from django.contrib.auth.models import User


class Profile(models.Model):
    avatar = models.ImageField(null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'profile'

    def __str__(self):
        return self.user


class Tag(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'tag'

    def __str__(self):
        return self.name


class QuestionManager(models.Manager):
    def get_new(self):
        return self.order_by('-created_at')

    def get_hot(self):
        return self.annotate(num_likes=Count("questionlike__question")).filter(num_likes__gt=15)


class Question(models.Model):
    title = models.CharField(max_length=255)
    text = models.CharField(max_length=1024)
    tags = models.ManyToManyField(Tag)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = QuestionManager()

    class Meta:
        app_label = 'question'

    def __str__(self):
        return self.title


class Answer(models.Model):
    title = models.CharField(max_length=255)
    text = models.CharField(max_length=1024)
    truth_checkbox = models.BooleanField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'answer'

    def __str__(self):
        return self.title

class AnswerLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    answer = models.ForeignKey(Answer, on_delete=models.PROTECT)

    class Meta:
        app_label = 'answer_like'
        constraints = [
            models.UniqueConstraint(fields=['user', 'answer'], name='unique_answerlike_user')
        ]

    def __str__(self):
        return self.user

class QuestionLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    question = models.ForeignKey(Question, on_delete=models.PROTECT)
    name_of_me = 'andrey'
    class Meta:
        app_label = 'question_like'

        constraints = [
            models.UniqueConstraint(fields=['user', 'question'], name='unique_questionlike_user')
        ]
    def __str__(self):
        return self.user
