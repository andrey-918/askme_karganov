from django.db import models
from django.db.models import Count
from django.contrib.auth.models import User
from django.db.models import Sum, Prefetch
from datetime import date


class Profile(models.Model):
    avatar = models.ImageField(null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class TagManager(models.Manager):
    def get_popular(self):
        return self.order_by('-tag_posts')[:10]



class Tag(models.Model):
    name = models.CharField(max_length=255)
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tag_posts = models.IntegerField(default=0)

    objects = TagManager()

    def __str__(self):
        return self.name


class QuestionManager(models.Manager):
    def get_new(self):
        return self.order_by('-created_at')

    def get_hot(self):
        return self.order_by('-answer_count')

    def get_by_tag(self, tag):
        return self.filter(tags__id=tag).order_by('-created_at')


class Question(models.Model):
    question_id = models.IntegerField(default=0)
    title = models.CharField(max_length=255)
    text = models.CharField(max_length=1024)
    tags = models.ManyToManyField(Tag, blank=True)
    creator = models.ForeignKey(Profile, on_delete=models.CASCADE)
    answer_count = models.IntegerField(default=0)
    carma = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = QuestionManager()


    def calculate_rating(self):
        score_sum = QuestionLike.objects.filter(question_id=self.id).aggregate(Sum('value', default=0))
        return score_sum['value__sum']

    def __str__(self):
        return self.title





class Answer(models.Model):
    title = models.CharField(max_length=255)
    text = models.CharField(max_length=1024)
    truth_checkbox = models.BooleanField()
    creator = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    carma = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def calculate_rating(self):
        score_sum = AnswerLike.objects.filter(answer_id=self.id).aggregate(Sum('value', default=0))
        return score_sum['value__sum']



    def __str__(self):
        return self.title

class AnswerLike(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    value = models.IntegerField(default=0)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'answer'], name='unique_user_answer')
        ]

    def __str__(self):
        return str(self.answer_id)

class QuestionLike(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    value = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'question'], name='unique_user_question')
        ]

    def __str__(self):
        return str(self.question_id)
