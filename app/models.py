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
    title = models.CharField(max_length=255)
    likes_count = models.IntegerField(default=0, verbose_name='Likes')
    dislikes_count = models.IntegerField(default=0, verbose_name='Dislikes')
    text = models.CharField(max_length=1024)
    tags = models.ManyToManyField(Tag, blank=True)
    creator = models.ForeignKey(Profile, on_delete=models.CASCADE)
    answer_count = models.IntegerField(default=0)
    carma = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = QuestionManager()

    def get_url(self):
        return reverse('question', kwargs={'id': self.id})
    def calculate_rating(self):
        score_sum = QuestionLike.objects.filter(id=self.id).aggregate(Sum('value', default=0))
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
    likes_count = models.IntegerField(default=0, verbose_name='Likes')
    dislikes_count = models.IntegerField(default=0, verbose_name='Dislikes')
    is_correct = models.BooleanField(default=False, verbose_name='Is correct')

    objects = QuestionManager()

    def calculate_rating(self):
        score_sum = AnswerLike.objects.filter(id=self.id).aggregate(Sum('value', default=0))
        return score_sum['value__sum']



    def __str__(self):
        return self.question.title
class QuestionLike(models.Model):
    question = models.ForeignKey('Question', on_delete=models.CASCADE, verbose_name='Question')
    profile_id = models.ForeignKey('Profile', on_delete=models.CASCADE, verbose_name='Profile')
    is_like = models.BooleanField(default=True, verbose_name='Like or dislike')

    def __str__(self):
        action = 'Disliked'
        if self.is_like:
            action = 'Liked'
        return self.profile_id.user.get_username() + ' ' + action + ' "' + self.question.title + '"'

    def save(self, *args, **kwargs):
        if not self.pk:
            if self.is_like:
                self.question.likes_count += 1
                self.question.carma += 1
            else:
                self.question.dislikes_count += 1
                self.question.carma -= 1
            self.question.save()
        super(QuestionLike, self).save(*args, **kwargs)
        return self.question.carma

    def delete(self, *args, **kwargs):
        if self.is_like:
            self.question.likes_count -= 1
            self.question.carma -= 1
        else:
            self.question.dislikes_count -= 1
            self.question.carma += 1
        self.question.save()
        super(QuestionLike, self).delete(*args, **kwargs)
        return self.question.carma

    def change_mind(self):
        if self.is_like:
            self.question.likes_count -= 1
            self.question.dislikes_count += 1
            self.question.carma -= 2
        else:
            self.question.likes_count += 1
            self.question.dislikes_count -= 1
            self.question.carma += 2
        self.is_like = not self.is_like
        self.save()
        self.question.save()
        return self.question.carma

    class Meta:
        unique_together = ('question', 'profile_id')
        verbose_name = 'Question like'
        verbose_name_plural = 'Questions likes'


class AnswerLike(models.Model):
    answer_id = models.ForeignKey('Answer', on_delete=models.CASCADE, verbose_name='Answer')
    profile_id = models.ForeignKey('Profile', on_delete=models.CASCADE, verbose_name='Profile')
    is_like = models.BooleanField(default=False, verbose_name='Like or dislike')

    def __str__(self):
        action = 'Disliked'
        if self.is_like:
            action = 'Liked'
        return self.profile_id.user.get_username() + ' ' + action + ' "' + self.answer_id.text + '"'

    def save(self, *args, **kwargs):
        if not self.pk:
            if self.is_like:
                self.answer_id.likes_count += 1
                self.answer_id.carma += 1
            else:
                self.answer_id.dislikes_count += 1
                self.answer_id.carma -= 1
            self.answer_id.save()
        super(AnswerLike, self).save(*args, **kwargs)
        return self.answer_id.carma

    def delete(self, *args, **kwargs):
        if self.is_like:
            self.answer_id.likes_count -= 1
            self.answer_id.carma -= 1
        else:
            self.answer_id.dislikes_count -= 1
            self.answer_id.carma += 1
        self.answer_id.save()
        super(AnswerLike, self).delete(*args, **kwargs)
        return self.answer_id.carma

    def change_mind(self):
        if self.is_like:
            self.answer_id.likes_count -= 1
            self.answer_id.dislikes_count += 1
            self.answer_id.carma -= 2
        else:
            self.answer_id.likes_count += 1
            self.answer_id.dislikes_count -= 1
            self.answer_id.carma += 2
        self.is_like = not self.is_like
        self.save()
        self.answer_id.save()
        return self.answer_id.carma

    class Meta:
        unique_together = ('answer_id', 'profile_id')
        verbose_name = 'Answer like'
        verbose_name_plural = 'Answers likes'