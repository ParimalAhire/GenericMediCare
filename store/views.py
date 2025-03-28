from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .forms import SignUpForm
from django.contrib import messages
from .models import Medicine

def home(request):
    products = Medicine.objects.all()
    return render(request, 'home.html', {'products':products})

def about(request):
    return render(request, 'about.html', {})

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            messages.success(request, 'You have been successfully logged in')
            return redirect('home')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')

    else:
        return render(request, 'login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out')
    return redirect('home')

def register_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            # Log the user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'You have been successfully registered! You are now logged in Welcome to our store')
            return redirect('home')
        else:
            print(form.errors)
            messages.error(request, f"An error has occurred during registration: {form.errors.as_text()}")
            return redirect('register')
    
    else:
        return render(request, 'register.html', {'form':form})

def suggest_alternatives(request):
    if request.method == "POST":
        prescribed_composition = request.POST.get("composition")  # Get composition from form
        alternatives = Medicine.find_alternatives(prescribed_composition)
        return render(request, "suggest_alternatives.html", {"alternatives": alternatives})
    
    return render(request, "upload_prescription.html")