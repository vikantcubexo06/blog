import django

from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Info(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, max_length=10)
    firstname = models.CharField(max_length=15)
    lastname = models.CharField(max_length=15)
    # email = models.EmailField()
    gender = models.CharField(max_length=10)
    age = models.IntegerField()
    bio = models.CharField(max_length=500)
    imag = models.ImageField(default="default.png", upload_to='static/profile_image')

    def __str__(self):
        return str(self.username)


class Blog(models.Model):
    user = models.ForeignKey(Info, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    write_blog = models.TextField()
    approval = models.BooleanField(default=False)
    Date = models.DateField(default=django.utils.timezone.now, null=False)

    # comment = models.ForeignKey(CommentPost, on_delete=models.CASCADE, null=True )

    # comment_reply = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        ordering = ['Date']

    def __str__(self):
        return str(self.user)


class CommentPost(models.Model):
    comment_text = models.CharField(max_length=500, null=True)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)


class ReplyComment(models.Model):
    comment_text = models.ForeignKey(CommentPost, on_delete=models.CASCADE, null=True)
    reply = models.CharField(max_length=400)


class Query(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField()
    mobile = models.PositiveIntegerField()
    query = models.CharField(max_length=2000)
