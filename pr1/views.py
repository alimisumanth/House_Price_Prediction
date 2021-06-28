from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse

from .form import CreateUserForm
from .database import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout




# user homepage

def upload(request):
    if request.method == 'POST':
        return render(request, 'input.html', {'data': table_creation(request)})
    else:
        if request.user.is_authenticated:
            return render(request, 'input.html')
        else:
            return redirect('pr1:login')





# logout method
def logoutpage(request):
    try:
        logout(request)
        request.session.clear()  # deleting the session of user
    except:
        return redirect('pr1:index')  # redirecting to login page
    return redirect('pr1:login')  # redirecting to login page


def home(request):
    return render(request, 'home.html')


# login method
def loginpage(request):
    """ if user submits the credentials  then it check if they are valid or not
                    if it is valid then it redirects to user home page """
    if request.user.is_authenticated:
        return redirect('pr1:home')
    else:

        if request.method == 'POST':

            username = request.POST.get('username')
            password = request.POST.get('password')
            print(username,password)


            user = authenticate(request, username=username, password=password)
            print(user)
            # chek user exist
            if user is not None:
                login(request, user)
                return redirect('pr1:home')
            else:
                messages.info(request, 'User Name or Password is incorrect')
        context = {}
        return render(request, 'login.html', context)


# user registration method
def register(request):
    if request.user.is_authenticated:
        return redirect('pr1:home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user1 = form.save()

                user = form.cleaned_data.get('username')
                print(user1.password)
                messages.success(request, 'Account was created for ' + user)
                return redirect('pr1:login')
        context = {'form': form}
        return render(request, 'register.html', context) # redirecting to registration page


# ml model

def model(request):
    if request.method == 'POST':
        return render(request, 'result.html', {'data': model_training()})
    else:
          if request.user.is_authenticated:
              return render(request, 'model.html')
          else :
              return redirect('pr1:login')

def eda(request):
    statisticalinfo()
    return render(request, 'stats.html')





