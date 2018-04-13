from django.shortcuts import render
from .forms import UserForm, UserInfoForm, TopicForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View, TemplateView, ListView, DetailView
from . import models

# Create your views here.

class OwnTopicListView(ListView):

    model = models.Topic
    template_name = 'own_topics.html'
    context_object_name = 'topics'


    def get_queryset(self):
        return models.Topic.objects.filter(author=self.request.user)


class TopicListView(ListView):

    model = models.Topic
    template_name = 'topics.html'
    context_object_name = 'topics'

class TopicDetailView(DetailView):

    model = models.Topic
    template_name = 'topic_detail.html'
    context_object_name = 'topic'

    def post(self, request, **kwargs):
        data = request.POST.get('comment')
        topic_id = request.POST.get('topic_id')
        topic = models.Topic.objects.get(id__exact=topic_id)
        user = request.user

        comment = models.Comment()
        comment.topic = topic
        comment.content = data
        comment.author = user
        
        comment.save()

        pk = topic_id
        return HttpResponseRedirect(reverse('app:topic_detail', args=(pk)))



def to_login(request):

    return render(request, "redirect_login.html")

@login_required
def new_topic(request):

    if request.method == 'POST':
        topic_form = TopicForm(data=request.POST)
        author = request.user

        topic = topic_form.save(commit=False)
        topic.author = author
        topic.likes = 0
        topic.favorates = 0
        topic.save()
        #split tags
        tag_data = topic_form.cleaned_data['tags']
        tags = tag_data.split()
        for tag in tags:
            item = models.Tag()
            item.label = tag
            item.save()
            topic.tags.add(item)
        topic.save()
        return HttpResponseRedirect(reverse('app:topics'))

    else:
        topic_form = TopicForm()
        return render(request, 'new_topic.html', {'topic_form':topic_form})


def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username = username, password = password)

        if user:
            login(request, user)
            return HttpResponseRedirect(reverse('app:topics'))
        else:
            return HttpResponse("Woops!Your username doesn't match password!")
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('app:topics'))
        return render(request, 'login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('app:user_login'))

def register(request):

    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        userInfo_form = UserInfoForm(data=request.POST)
        if user_form.is_valid() and userInfo_form.is_valid():
            
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            info = userInfo_form.save(commit=False)
            info.user = user
            info.save()
            registered = True
            login(request, user)
        else:
            print(user_form.errors, userInfo_form.errors)
    else:
        user_form = UserForm()
        userInfo_form = UserInfoForm()


    return render(request, "register.html", 
                            {'user_form' : user_form,
                             'userInfo_form' : userInfo_form,
                             'registered' : registered})

def homepage(request):
    return render(request, 'homepage.html')

@login_required
def increase_likes(request):
    topic_id = -1
    if request.method == "GET":
        topic_id = request.GET.get('id')
    topic = models.Topic.objects.get(id=int(topic_id))
    topic.likes += 1
    topic.save()
    return HttpResponse(topic.likes)

@login_required
def increase_favorates(request):
    topic_id = -1
    if request.method == "GET":
        topic_id = request.GET.get('id')
    topic = models.Topic.objects.get(id=int(topic_id))
    topic.favorates += 1

    user = request.user
    topic.favorate_by.add(user)

    topic.save()
    return HttpResponse(topic.favorates)


class FavorateListView(ListView):
    model = models.Topic
    template_name = 'favorate_topics.html'
    context_object_name = 'topics'

    def get_queryset(self):
        user = self.request.user
        topics = user.topic_set.all()   #topic_set  -> auto create by manytomany fields
        return topics
