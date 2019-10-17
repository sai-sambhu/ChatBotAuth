from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Authenticationss(models.Model):
    Name=models.CharField(blank=True,max_length=1000)
    PhoneNumber=models.CharField(blank=True,max_length=1000)
    Email=models.CharField(blank=True,max_length=1000)
    Answers=models.CharField(blank=True,max_length=5000)
    OTP=models.CharField(blank=True,max_length=5)



class ChatBotAdmin(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    #additional
    
    
    def __str__(self):
        return self.user.username


class QandAModels(models.Model):
    Questions=models.CharField(blank=True,max_length=1000)
    Answers=models.CharField(blank=True,max_length=5000)    
    

class StudentBotUsersDetails(models.Model):
    Name=models.CharField(blank=True,max_length=1000)
    PhoneNumber=models.CharField(blank=True,max_length=1000)
    Email=models.CharField(blank=True,max_length=1000)
    Answers=models.CharField(blank=True,max_length=5000)
    
    
