from django.shortcuts import render, redirect
from .forms import RegisterUserForm, LoginUserForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Accounts

# register new user


def user_register(requset):
    if (requset.method == 'POST'):
        form = RegisterUserForm(requset.POST)
        if (form.is_valid()):
            cd = form.cleaned_data

            user = User.objects.create_user(
                username=cd['username'], email=cd['email'], password=cd['password'])
            user.first_name = cd['first_name']
            user.last_name = cd['last_name']
            user.save()
            account = Accounts.objects.create(user=user, charge=5)
            messages.success(
                requset, 'user registered successfully', extra_tags='success')
            return redirect('login')
    else:
        form = RegisterUserForm()

    return render(requset, 'register.html', context={'form': form})


# login existing user


def user_login(request):
    if (request.method == 'POST'):
        form = LoginUserForm(request.POST)

        if (form.is_valid()):
            cd = form.cleaned_data

            user = authenticate(
                request, username=cd['username'], password=cd['password'])
            if user is not None:
                # user logged in successfully
                login(request, user)
                messages.success(
                    request, 'You have logged in successfully', extra_tags='success')
                return redirect('home')

            else:
                messages.error(
                    request, 'Your password or email is wrong', extra_tags='danger')

    else:
        form = LoginUserForm()

    return render(request, 'login.html', context={'form': form})


def user_logout(request):
    logout(request)
    messages.success(request, 'You are successfully logged out', 'success')
    return redirect('login')


def me(request):
    if (request.user.is_authenticated):
        data = {
            'name': request.user.first_name,
            'charge': Accounts.objects.get(user=request.user).charge
        }
        return render(request, 'me.html', context=data)
    else:
        messages.success(request, 'You need to login first', 'danger')
        return render('login')
