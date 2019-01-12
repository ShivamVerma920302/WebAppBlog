from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login

# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm()
        args ={
            'form': form
        }
        if form.is_valid():
            user = form.save()
            print(user)
            auth_login(request, user)
            return redirect('home')
        return render(request, 'signup.html', args)
    else:
        form = UserCreationForm()
        args ={
            'form': form
        }
        return render(request, 'signup.html', args)