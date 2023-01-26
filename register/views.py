
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User , auth
from django.contrib.auth import  logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    if request.method =='POST':
        first_name =request.POST['first_name']
        last_name =request.POST['last_name']
        username =request.POST['username']
        passwrod1 =request.POST['password1']
        password2 =request.POST['password2']
        email =request.POST['email']

        if passwrod1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username Taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'Email Taken')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username,password=passwrod1,email=email,first_name=first_name,last_name=last_name)
                user.save();
                print('user created')
                return redirect('login')
           
        else:
            messages.info(request,'Password not matching')
            
            return redirect('register')
        # return redirect('/')
    else:
        return render(request,'index.html')

    # return render(request,'index.html' )


def login(request):

    if request.method== 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect("home")
        else:
            messages.info(request,'invalid credentials')
            return redirect('login')
    else:
         return render(request,'login.html')


    # return render(request,'login.html')

@login_required(login_url='login')
# @cache_control(no_cache = True,must_revalidate = False,no_store=True)
def home(request):


    return render(request,'home.html')
   


def logout(request):
    auth.logout(request)
    return redirect('login')