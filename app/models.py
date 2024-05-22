from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse


class Profile(models.Model):
    avatar = models.ImageField(upload_to='avatars/', default='avatars/avatar.png')
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class TagManager(models.Manager):
    def get_popular(self):
        return self.order_by('-tag_posts')[:10]

    def create_question(self, tags_list):
        tags = self.filter(name__in=tags_list)
        for tag in tags:
            tag.tag_posts += 1
            tag.save()
        return tags





class Tag(models.Model):
    name = models.CharField(max_length=255)
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

    def get_url(self):
        return reverse('question', kwargs={'question_id': self.id})
    def calculate_rating(self):
        score_sum = QuestionLike.objects.filter(question_id=self.id).aggregate(Sum('value', default=0))
        return score_sum['value__sum']

    def __str__(self):
        return self.title







class Answer(models.Model):
    text = models.CharField(max_length=1024)
    creator = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    carma = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = QuestionManager()

    def calculate_rating(self):
        score_sum = AnswerLike.objects.filter(answer_id=self.id).aggregate(Sum('value', default=0))
        return score_sum['value__sum']



    def __str__(self):
        return self.question.title

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

