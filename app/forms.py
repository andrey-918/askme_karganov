from django import formsfrom django.core.exceptions import ValidationErrorfrom django.contrib.auth.models import Userimport djangofrom django.forms import TextInput, Textarea, FileInputfrom app.models import *from django.forms import PasswordInputfrom django.contrib.auth.password_validation import validate_passwordfrom django import formsclass LoginForm(forms.Form):    username = forms.CharField(max_length=30)    password = forms.CharField()class RegisterForm(forms.ModelForm):    password = forms.CharField(widget=forms.PasswordInput)    repeat_password = forms.CharField(widget=forms.PasswordInput)    class Meta:        model = User        fields = ['username', 'email', 'password']    def clean(self):        password = self.cleaned_data['password']        repeat_password = self.cleaned_data['repeat_password']        if not password or not repeat_password:            return        if password != repeat_password:            self.add_error('repeat_password', 'Passwords do not match!')            print('not matched')            return        return self.cleaned_data    def clean_username(self):        if User.objects.filter(username=self.cleaned_data['username']).exists():            self.add_error('username', 'This username is already in use')        return self.cleaned_data['username']    def clean_email(self):        if User.objects.filter(email=self.cleaned_data['email']).exists():            self.add_error('email', 'This email is already in use')        return self.cleaned_data['email']    def save(self, **kwargs):        user = User.objects.create_user(self.cleaned_data['username'], self.cleaned_data['email'],                                        self.cleaned_data['password'])        Profile.objects.create(user=user)        return userclass AskForm(forms.ModelForm):    tags = forms.CharField(required=False)    class Meta:        model = Question        fields = ['title', 'text']    widgets = {        'title': TextInput(),        'text': Textarea(),    }    def __init__(self, creator=None, **kwargs):        self._creator = creator        super(AskForm, self).__init__(**kwargs)    def clean_tags(self):        self.tags = self.cleaned_data['tags'].split()        if len(self.tags) > 25:            self.add_error(None, 'Use no more than 25 tags')            raise forms.ValidationError('Use no more than 25 tags')        return self.tags    def save(self, **kwargs):        published_question = Question()        published_question.creator = self._creator        published_question.title = self.cleaned_data['title']        published_question.text = self.cleaned_data['text']        published_question.save()        for tag in self.cleaned_data['tags']:            if not Tag.objects.filter(name=tag).exists():                Tag.objects.create(name=tag)        published_question.tags.set(Tag.objects.create_question(self.tags))        return published_questionclass SettingsForm(forms.ModelForm):    username = forms.CharField()    email = forms.CharField(required=False)    first_name = forms.CharField(required=False)    last_name = forms.CharField(required=False)    avatar = forms.ImageField(required=False)    class Meta:        model = User        fields = ['username', 'email', 'first_name', 'last_name', 'avatar']    def clean(self):        cleaned_data = super().clean()        profiles = Profile.objects.all()        for profile in profiles:            user = profile.user            if user.username == cleaned_data['username'] and user.username != profile.user.username:                self.add_error(None, "This username is already taken")            elif user.email == cleaned_data['email'] and user.username != profile.user.username:                self.add_error(None, "This email is already taken")    def save(self, *args, **kwargs):        user = super().save(*args, **kwargs)        user.profile.save()        return userclass AnswerForm(forms.ModelForm):    class Meta:        model = Answer        fields = ['text']    def __init__(self, creator=None, **kwargs):        self._creator = creator        super(AnswerForm, self).__init__(**kwargs)    def save(self, **kwargs):        published_answer = Answer()        published_answer.creator = self._creator        published_answer.text = self.cleaned_data['text']        published_answer.save()        return published_answer