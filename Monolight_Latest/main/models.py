from os import times
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    desg = models.CharField(max_length=50, default="")
    image = models.ImageField(upload_to="images", default="")
    branch = models.CharField(max_length=10, default="MCA")
    sem = models.IntegerField(default=1)
    add_line_1 = models.CharField(max_length=50)
    add_line_2 = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pin_code = models.CharField(max_length=20, default="")
    phone = models.CharField(max_length=15)
    dob = models.DateTimeField()
    join = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Request(models.Model):
    user_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    data = models.JSONField()
    file = models.FileField(upload_to="documents", default="")
    time = models.DateTimeField(auto_now_add=True)
    is_pending = models.BooleanField(default=True)


class Notification(models.Model):
    req_id = models.ForeignKey(Request, on_delete=models.CASCADE)
    user_id = models.IntegerField()
    is_approved = models.BooleanField(default=False)
    message = models.CharField(max_length=100)
    time = models.DateTimeField(auto_now_add=True)


class Attendance(models.Model):
    user_id =  models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    subject = models.CharField(max_length=10, default='CA401')
    date = models.DateField()
    in_time = models.TimeField();
    is_absent = models.BooleanField(default=True)
    def __str__(self):
        return f'{self.user_id.user.username} {self.date}'