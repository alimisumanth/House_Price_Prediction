from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import User

# user homepage
def profile(request):
    if 'user' in request.session:
        return render(request, 'profile.html')# redirects to homepage if user login successfull
    else:
        return redirect('pr1:index')# if user is not logged then redirects to login page
# logout method
def logout(request):
    try:
        del request.session['user']# deleting the session of user
    except:
        return redirect('pr1:index')# redirecting to login page
    return redirect('pr1:index')# redirecting to login page
#login menthod
def login(request):
    if request.method == 'POST':# if user submits the credentials  then it check if they are valid or not if it is valid then it redirects to user home page
        uname = request.POST.get('username')# retriving username from login form
        pwd = request.POST.get('password')# retriving password from login form
        check_user = User.objects.filter(username=uname, password=pwd)# check user details in user db
        if check_user:# checks user is valid or not
            request.session['user'] = uname
            return redirect('pr1:profile')#redirecting to homepage
        else:
            return HttpResponse('Please enter valid Username or Password.')# if the user details doesn't match it will prompt invalid credentials
    return render(request, 'login.html')

#user registration method
def register(request):
    if request.method == 'POST':
        uname = request.POST.get('username')# Retriving username from registration form
        pwd = request.POST.get('password')# Retriving password from registration form
        email=request.POST.get("email")# Retriving email_id from registration form
        mobile=request.POST.get('mobile_number')#Retriving mobile number from registration form
        if User.objects.filter(username=uname).count() > 0:# checks if username already exits or not
            return HttpResponse('Username already exists.')
        else:
            user = User(username=uname, password=pwd,email=email)# if username doesnot exist then it will create a new user with provided details
            user.save()# saves user details in user db
            return redirect('pr1:index')#redirects to login page
    else:
         return render(request, 'register.html')#redirecting to registration page
