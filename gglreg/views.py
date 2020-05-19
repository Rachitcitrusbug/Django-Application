from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.sessions.models import Session

# Create your views here.


def login(request):
    if request.session.has_key('is_logged'):
        return redirect('home')

    if request.method == 'POST':
        email = request.POST['email']

        user = auth.authenticate(email=email)

        if user is not None:
            request.session['is_logged'] = True
            auth.login(request, user)
            return redirect('welcome')
        else:
            messages.info(request, 'Unregistered/Invalid Email ID !')
            return redirect('login')

    else:
        return render(request, 'login.html')


def signup(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']+'@gmail.com'
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if User.objects.filter(username=username).exists():
            messages.info(request, 'Email address already taken!')
            return redirect('signup')

        else:
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, password=password1)
            user.save()
            print("***SUCCESSFULL***")
            return redirect('/')

    else:
        return render(request, 'signup.html')


def welcome(request):
    if request.session.has_key('is_logged'):
        return redirect('home')

    if request.method == 'POST':
        password = request.POST['password']

        user = auth.authenticate(password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Invalid password !')
            return redirect('welcome')

    else:
        return render(request, 'welcome.html')