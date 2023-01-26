from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.hashers import make_password

# Create your views here.

def admin_login(request):
    try:
        if request.user.is_authenticated:
            return redirect('dashboard')


        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user_obj=User.objects.filter(username = username)
            if not user_obj.exists ():
                messages.info(request,'!!Account not found!!    ')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            user_obj=authenticate(username = username,password = password)
            if user_obj and user_obj.is_superuser:
                login(request, user_obj)
                return redirect('dashboard')

            messages.info(request, 'Invalid Password')
            return redirect('admin_login')

        return render(request,'adminlogin.html')

    except Exception as e:
        print(e)

@login_required(login_url='admin_login')
def dashboard(request):

    objs=User.objects.all
    return render(request,'dashboard.html',{'objs':objs})


def logout(request):
    auth.logout(request)
    return redirect('/')


@login_required(login_url='admin_login')
def add_user(request):
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
                return redirect('adduser')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'Email Taken')
                return redirect('adduser')
            else:
                user = User.objects.create_user(username=username,password=passwrod1,email=email,first_name=first_name,last_name=last_name)
                user.save();
                return redirect('dashboard')
           
        else:
            messages.info(request,'Password not matching')
            
            return redirect('adduser')
        
    else:
        return render(request,'adduser.html')
    # return render(request,'adduser.html')


@login_required(login_url='admin_login')
def delete_user(request,id):
    usr=User.objects.get(id=id)
    usr.delete()
    return redirect('dashboard')

@login_required(login_url='admin_login')
def update(request,id):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        superusr =request.POST.getlist('checks')


        try:
            if superusr[0] == '1':
                
                usr =User(
                    id = id,
                    username = username,
                    email = email,
                    first_name = first_name,
                    last_name = last_name,
                    password = make_password(password),
                    is_superuser = True
                )
        # password = request.POST['password']
        # pass2 = request.POST['pass2']

        # if User.objects.filter(username=username).exists():
        #     messages.info(request,f'Username {username} is already taken')
        #     return redirect('update',id)
        # elif User.objects.filter(email = email).exists():
        #      messages.info(request,f'{email} is already registered.')
        #      return redirect('update',id)

        # if first_name == '' or email == '' or last_name == ' ' or username==' ':
        #     messages.info(request,'Fill all the fields ')
        #     return redirect('update',id)
        except:
            usr =User(
                    id = id,
                    username = username,
                    email = email,
                    first_name = first_name,
                    last_name = last_name,
                    password = make_password(password),
                )
        usr.save()
        return redirect('dashboard')

    else:
        usr=User.objects.get(id=id)
        return render(request,'edituser.html',{'usr':usr})
        
    
def search(request):
    if request.method=='GET':
        searchterm =request.GET.get('searchterm')
        objs=User.objects.filter(username__icontains=searchterm)
        return render(request,'dashboard.html',{'objs':objs})
    else:
        print('Nothing similar')
        return redirect('dashboard')