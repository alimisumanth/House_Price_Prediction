from django.shortcuts import render, redirect
from .form import CreateUserForm
from .database import SQLiteDB
from django.contrib import messages
import os
from .mlmodel import mlmodel
from .utils import utils
from django.contrib.auth import authenticate, login, logout
import pandas as pd
import sqlite3
from .logger import Logger


logger = Logger()
mlmodel = mlmodel()

# user homepage
def upload(request):
    if request.method == 'POST':
        file = request.FILES['input-b6b[]']
        filename=file.name
        fileobject = open("Logs.txt", 'a+')
        if filename[filename.find('.'):] != '.csv':
            logger.log(file_object=fileobject, log_message='Invalid input format')
            fileobject.close()
            return render(request, 'input.html', {'input_file': 'Please upload the file in csv format'})
        logger.log(file_object=fileobject, log_message='Pushing input data to database')
        fileobject.close()
        return render(request, 'input.html', {'data': SQLiteDB.table_creation(SQLiteDB(),request), 'stats': 'Click here to view statistical insights of historical data'})
    else:
        if request.user.is_authenticated:
            return render(request, 'input.html')
        else:
            return redirect('HousePricing:login')


# logout method
def logoutpage(request):
    try:
        fileobject = open("Logs.txt", 'a+')
        SQLiteDB.tabledeletion(SQLiteDB())
        logger.log(file_object=fileobject, log_message="Logout successfull")
        fileobject.close()
        logout(request)
        request.session.clear()  # deleting the session of user
    except Exception as e:
        logger.log(file_object=fileobject, log_message=e)
        fileobject.close()
        return redirect('HousePricing:login')  # redirecting to login page
    return redirect('HousePricing:login')  # redirecting to login page


def home(request):
    if request.user.is_authenticated:
        return render(request, 'home.html')
    else:
        return redirect('HousePricing:login')


# login method
def loginpage(request):
    """ if user submits the credentials  then it check if they are valid or not
                    if it is valid then it redirects to user home page """
    fileobject = open("Logs.txt", 'a+')
    if request.user.is_authenticated:
        logger.log(file_object=fileobject, log_message='User already logged in redirecting to homepage')
        fileobject.close()
        return redirect('HousePricing:home')
    else:

        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                logger.log(file_object=fileobject, log_message='User authentication success, redirecting to homepage')
                return redirect('HousePricing:home')
            else:
                logger.log(file_object=fileobject, log_message='User authentication failed')
                messages.info(request, 'User Name or Password is incorrect')
        context = {}
        fileobject.close()
        return render(request, 'login.html', context)


# user registration method
def register(request):
    if request.user.is_authenticated:
        fileobject = open("Logs.txt", 'a+')
        logger.log(file_object=fileobject, log_message='User already logged in redirecting to homepage')
        fileobject.close()
        return redirect('HousePricing:home')
    else:
        form = CreateUserForm()
        fileobject = open("Logs.txt", 'a+')
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)
                logger.log(file_object=fileobject, log_message='User account created successfully redirecting to login page')
                fileobject.close()
                return redirect('HousePricing:login')
        context = {'form': form}
        fileobject.close()
        return render(request, 'register.html', context)  # redirecting to registration page


# ml model
def model(request):
        if request.user.is_authenticated:
            fileobject = open("Logs.txt", 'a+')
            with sqlite3.connect("db.sqlite3") as c:
                try:
                    data = pd.read_sql_query('SELECT * from House_pricing', c)
                    if data is not None:
                        logger.log(file_object=fileobject, log_message='Ml model prediction')
                        fileobject.close()
                        temp=mlmodel.model_prediction()
                        return render(request, 'model.html',temp )
                except Exception as e:
                    fileobject.close()
                    return render(request, 'result.html', {'data':'Please Upload an input file to continue'})
        else:
            return redirect('HousePricing:login')




def eda(request):
    if request.user.is_authenticated:
        if not os.path.exists("templates/eda.html"):
            utils.statisticalinfo()
        return render(request, 'eda.html')
    else:
        return redirect('HousePricing:login')


def charts(request):
    if request.user.is_authenticated:
        with sqlite3.connect("db.sqlite3") as c:
            try:
                data = pd.read_sql_query('SELECT * from predicted_House_pricing', c)
                if data.shape[0] > 0:
                    bar_col = data['YrSold'].value_counts()
                    values_b=bar_col.tolist()
                    names_b=list(map(str,bar_col.index.tolist()))
                    bardata=[{names_b[i]:values_b[i]} for i in range(len(names_b))]

                    pie_col=data['MSZoning'].value_counts()
                    values = pie_col.tolist()
                    names = list(map(str, pie_col.index.tolist()))
                    pie_data=[{'name':names[i],'y': values[i]} for i in range(len(names))]
                    return render(request, 'charts.html',{'bar_data': values_b,'names':names_b,'piedata':pie_data})
            except Exception as e :
                return render(request, 'result.html', {'data':'Please predict the input data to get the prediction insights'})
    else:
        return redirect('HousePricing:login')

def download(request):
    return utils.filedownload(utils())
def download_featureinfo(request):
    return utils.featuresinfo_download(utils())
