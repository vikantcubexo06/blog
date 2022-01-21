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

    def __str__(self):
        return str(self.user)
