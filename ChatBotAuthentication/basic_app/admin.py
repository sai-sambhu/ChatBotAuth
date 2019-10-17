from django.contrib import admin

# Register your models here.
from basic_app.models import ChatBotAdmin
from basic_app.models import QandAModels,StudentBotUsersDetails,Authenticationss

admin.site.register([ChatBotAdmin,QandAModels,StudentBotUsersDetails,Authenticationss])
