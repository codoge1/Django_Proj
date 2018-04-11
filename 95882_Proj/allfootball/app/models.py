from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    favorate_team = models.CharField(max_length=50)

    def __str__(self):
        return self.user.username

class Tag(models.Model):

    label = models.CharField(max_length = 20)

    def __str__(self):
        return self.label


class Topic(models.Model):

    title = models.CharField(max_length = 256)
    content = models.CharField(max_length = 3000)
    author = models.ForeignKey(User, related_name = 'author', on_delete=models.CASCADE)
    date = models.DateField(auto_now = False, auto_now_add = True)

    likes = models.BigIntegerField(blank=True, null=True)
    favorates = models.BigIntegerField(blank=True, null=True)
    favorate_by = models.ManyToManyField(User, blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True, null=True)


    def __str__(self):
        return self.title

class Comment(models.Model):

    content = models.CharField(max_length = 256)
    topic = models.ForeignKey(Topic, related_name = 'comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now = False, auto_now_add = True)

    def __str__(self):
        return 'Comment of ' + self.topic.title
