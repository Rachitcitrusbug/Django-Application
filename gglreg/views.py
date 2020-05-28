from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.sessions.models import Session
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .token_generator import account_activation_token
from django.core.mail import EmailMessage
# Create your views here.


def signup(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email_id = request.POST['username'] + '@gmail.com'
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if User.objects.filter(email=email_id).exists():
            messages.info(request, 'Email address already taken !')
            return redirect('signup')

        else:
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email_id, password=password1)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            email_subject = 'Activate Your Account'
            message = render_to_string('gglreg/email_message.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
            email = EmailMessage(email_subject, message, to=[email_id])
            email.send()
            print("***SUCCESSFULL***")
            return render(request, 'gglreg/account.html')

    else:
        return render(request, 'gglreg/signup.html')


def activate_account(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'gglreg/confirm.html')
    else:
        return render(request, 'gglreg/expire.html')


def login(request):
    #if request.session.has_key('is_logged'):
        #return redirect('home')
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if '@gmail.com' not in username:
            user = auth.authenticate(username=username, password=password)

            print(user)
            if user is not None:
                request.session['is_logged'] = True
                auth.login(request, user)
                return redirect('home')

            else:
                messages.info(request, 'Invalid credentials !')
                return redirect('login')

        elif username.endswith('@gmail.com'):
            username = username[:-10]
            user = auth.authenticate(username=username, password=password)

            print(user)
            if user is not None:
                request.session['is_logged'] = True
                auth.login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Invalid credentials !')
                return redirect('login')
        else:
            messages.info(request, 'Invalid credentials !')
            return redirect('login')
    else:
        return render(request, 'gglreg/login.html')


def account(request):
    return redirect('login')


def home(request):
    #if request.session.has_key('is_logged'):
    return render(request, 'blogapp/blog_home.html')
    #return redirect('login')


def logout(request):
    auth.logout(request)
    return redirect('home')
