from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm
from django.contrib.auth import login as auth_login, authenticate
from django.contrib import messages

# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
        return render(request, 'signup.html', {'form':form})
    else:
        form = SignUpForm()
        args ={
            'form': form
        }
        return render(request, 'signup.html', args)

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('home')
            else:
                messages.error(request,'Username or Password is incorrect. Please try again!')
                return render(request, 'login.html', {'form': form})
        else:
            return render(request, 'login.html', {'form': form})
    else:
        form = LoginForm()
        context = {'form': form}
        return render(request, 'login.html', context)

def userprofile(request):
     return render(request, 'my_account.html')