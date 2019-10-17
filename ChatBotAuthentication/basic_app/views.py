from django.shortcuts import render
from basic_app.forms import ChatBotAdminForm as UserForm 
from basic_app.models import QandAModels,StudentBotUsersDetails,Authenticationss
# Create your views here.

import threading
import random
import time

import smtplib 
from email.mime.text import MIMEText
s = smtplib.SMTP('smtp.gmail.com', 587)
s.starttls() 
s.login("chatbotstudentemail@gmail.com", "Wewillrockit12#")

from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

lock=threading.Lock()
OTP_list=list(range(11111, 99999))

emails=[]

def sendEmail():
    
    while True:
     time.sleep(1)
     try:  
        if emails!=[]:
            message = "Please don't share this OTP to anyone,your OTP is "+emails[0][1]+", enter the OTP in your bot page for Authentication."
            msg = MIMEText(message)
            msg['Subject'] = "OTP verification"
            s.sendmail("chatbotstudentemail@gmail.com", emails[0][0], msg.as_string()) 
            emails.pop(0)
            pass
     except:
           pass
t = threading.Thread(target = sendEmail) 
t.start()         
def index_Auth(request):
    st="This is a Authentication Bot Your information will be Registered only if you are authenticated,Please chat for authentication.If your information provided is wrong GoTo home page and chat again."
    if request.method=="POST":
        form=request.POST["count"]
        form=list(form.split("\t"))
        stud_auth = Authenticationss.objects.all()
        Otp=0
        obj=0
        for i in stud_auth:
            if(i.Email==form[0]):
                obj=i
                Otp=i.OTP
        if Otp==0:
          st="The provided Email is not in our Authentication entries please provide a valid email"
        else:
            if Otp==form[1]:
                b =Authenticationss.objects.get(Email=form[0])
                user=StudentBotUsersDetails.objects.get_or_create(Name=obj.Name,PhoneNumber=obj.PhoneNumber,Email=obj.Email,Answers=obj.Answers)
            
                b.delete()
                st="Your data is saved THANK YOU"
                pass
            else:
                st="Wrong OTP"
                
        
                
    return render(request,'botAuth.html',{"success":st})
    pass


def index(request):
    lock.acquire() 
    st="Please Chat with us and provide your details for analysis"
    my={}
    if request.method=="POST":
        form=request.POST["count"]
        Ans=""
        form=form.split('\t')
         
            
        SBU = StudentBotUsersDetails.objects.all()
        i=0
        for student in SBU:
            if form[1]==student.PhoneNumber:
                st="phone number Submitted is already taken"
                i=1
            if form[2]==student.Email:
                st="Email Submitted is already taken"
                i=1
        
        if i==0:
            for i in range(3,len(form)-1):
                Ans=Ans+'Q'+str(i-2)+")."+form[i]+"\t"
            otp=random.choice(OTP_list)
            emails.append([form[2],str(otp)])
         
            user=Authenticationss.objects.get_or_create(Name=form[0],PhoneNumber=form[1],Email=form[2],Answers=Ans,OTP=str(otp))
            st="You information is registered temporarily Goto authentication page."
            
        
    qlist=[]
    QA = QandAModels.objects.all()
    for student in QA:   
        Q=student.Answers
        Q=Q.replace("\t", "<br />")
        Q=student.Questions+"<br />"+Q
        qlist.append(Q)
        if(student.Answers==""):
            qlist.append("0")
        else:
             qlist.append(str(student.Answers.count(').')))
        
            
      
    my={"Questions" : [len(qlist)]+qlist,"success":st}
    lock.release()             
    return render(request,'bot.html',context=my) 
    pass

def chatbotadminindex(request):
    if request.method=="POST":
        CountQuestion = request.POST["count"]
        QandA=""
        QandAModels.objects.all().delete()
        for i in range(int(CountQuestion)):
            try:
                
                A = request.POST.getlist('answer'+str(i+1))
                for j in range(len(A)):
                   if A[j]!="": 
                    QandA=QandA+str(j+1)+').'+A[j]+"\t"    
                print(QandA)
                user=QandAModels.objects.get_or_create(Questions=request.POST["question"+str(i+1)],Answers=QandA)    
                QandA=""
                pass
            except:
                pass
        return render(request,'basic_app/success.html')    
          
    
   
    return render(request,'basic_app/index.html')
def register(request):
    logout(request)
    registered=False
    
    if request.method=="POST":
        
        user_form=UserForm(data=request.POST)
        
        if user_form.is_valid() :
            print("NAME: "+ user_form.cleaned_data['username'])
            user=user_form.save()
            user.set_password(user.password)
            user.save()
            
            registered=True
        else:
                print(user_form.errors)
    else:
         user_form=UserForm ()

    return render (request,'basic_app/registration.html',
                   {'user_form':user_form,
                    'registered':registered})          

 
    
@login_required   
def special(request):
     return HttpResponse("your are logged in")     
    
@login_required   
def user_logout(request):
     logout(request)
     return HttpResponseRedirect(reverse('chatbotadminindex'))    
   
def user_login(request):
    
       logout(request)    
       if request.method=="POST":
           username=request.POST.get('username')
           password=request.POST.get('password')
           
           user=authenticate(username=username,password=password)
          
           
           
           if user:
               
               if user.is_active:
                   login(request,user)
                   return HttpResponseRedirect(reverse('chatbotadminindex'))
               else :
                   return HttpResponse("ACCOUNT NOT ACTIVE")
           else:
               print("someone tried to login and failed")
               print(f'username: {username} and password: {password} ')
               return HttpResponse("invalid login details supplied!!")
       else:
            return render(request,'basic_app/login.html')


               