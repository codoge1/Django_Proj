from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    favorate_team = models.CharField(max_length=50)

    def __str__(self):
        return self.user.username

class Topic(models.Model):

    title = models.CharField(max_length = 256)
    content = models.CharField(max_length = 3000)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now = False, auto_now_add = True)

    def __str__(self):
        return self.title

class Comment(models.Model):

    content = models.CharField(max_length = 256)
    topic = models.ForeignKey(Topic, related_name = 'comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now = False, auto_now_add = True)

    def __str__(self):
        return 'Comment of ' + self.topic.title