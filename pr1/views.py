from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import User
from .database import *
from .models import User


# user homepage
def upload(request):
    if request.method == 'POST':
        return render(request, 'input.html', {'data': table_creation(request)})
    else:
        if 'user' in request.session:
            return render(request, 'input.html')  # redirects to homepage if user login successful
        else:
            return redirect('pr1:index')


# logout method
def logout(request):
    try:
        del request.session['user']  # deleting the session of user
    except e:
        return redirect('pr1:index')  # redirecting to login page
    return redirect('pr1:index')  # redirecting to login page

def home(request):
    return render(request, 'home.html')




# login method
def login(request):
    """ if user submits the credentials  then it check if they are valid or not
                    if it is valid then it redirects to user home page """

    if request.method == 'POST':
        uname = request.POST.get('username')  # retrieving username from login form
        pwd = request.POST.get('password')  # retrieving password from login form
        check_user = User.objects.filter(username=uname, password=pwd)  # check user details in user db
        if check_user:  # checks user is valid or not
            request.session['user'] = uname
            return render(request, 'home.html', {'user': uname})  # redirecting to homepage
        else:
            return HttpResponse('Please enter valid Username or Password.')  # if the user details doesn't match then  it will prompt invalid credentials
    return render(request, 'login.html')


# user registration method
def register(request):
    if request.method == 'POST':
        uname = request.POST.get('username')  # Retrieving username from registration form
        pwd = request.POST.get('password')  # Retrieving password from registration form
        email = request.POST.get("email")  # Retrieving email_id from registration form
        mobile = request.POST.get('mobile_number')  # Retrieving mobile number from registration form
        if User.objects.filter(username=uname).count() > 0:  # checks if username already exits or not
            return HttpResponse('Username already exists.')
        else:
            user = User(username=uname, password=pwd,
                        email=email, mobile=mobile)  # if username does not exist then it will create a new user with provided details
            user.save()  # saves user details in user db
            return redirect('pr1:index')  # redirects to login page
    else:
        return render(request, 'register.html')  # redirecting to registration page


# ml model
def model(request):
    if request.method == 'POST':
        return render(request, 'result.html', {'data': model_training()})
    else:
        if 'user' in request.session:
            return render(request, 'model.html')  # redirects to homepage if user login successful
        else:
            return render(request, 'login.html')
