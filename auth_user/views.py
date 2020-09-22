from django.shortcuts import render
from django.shortcuts import redirect

from django.contrib import auth
from django.contrib.auth.models import User

from .forms import AuthForm


def sign_up(request):
    if request.method == 'POST':
        form = AuthForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']

            user = User.objects.create_user(
                username=username,
                password=password
            )

            user.save()
            return redirect('login')
    else:
        if request.user.is_authenticated:
            return redirect('index')
        form = AuthForm()
        context = {'form': form}
        return render(request, 'auth/signup.html', context=context)


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None and user.is_active:
            auth.login(request, user)
            return redirect('index')

    else:

        if request.user.is_authenticated:
            return redirect('index')

    form = AuthForm()
    context = {'form': form}
    template = 'auth/login.html'

    return render(request, template, context)


def logout(request):
    auth.logout(request)
    return redirect('login')
