from django import  forms
from django.contrib.auth.models import User
from .models import UserInfo, Topic

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name',)

class UserInfoForm(forms.ModelForm):

    class Meta():
        model = UserInfo
        fields = ('favorate_team',)

class TopicForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea)
    tags = forms.CharField(label="Tags (Use single space to split several tags)", widget=forms.TextInput(attrs={'placeholder':'Tags'}))
    class Meta():
        model = Topic
        fields = ('title', 'content',)