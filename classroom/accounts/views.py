from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from .models import User
from django.contrib.auth.decorators import login_required
from .decorators import teacher_required,student_required
from django.http import HttpResponseForbidden
from .forms import RegisterForm
from django.contrib import messages
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
        else:
            return render(request, 'accounts/register.html', {'form': form})
            role=request.POST['role']
    return render(request, 'accounts/register.html')
# Create your views here.
def user_login(request):
    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        
        if user:
            login(request, user)
            return redirect('dashboard') 
        else :
            messages.error(request, "Invalid email or password.")
    return render(request, 'accounts/login.html')


@login_required
def dashboard(request):
    if request.user.role == 'teacher':
        return redirect('teacher_dashboard')
    return redirect('student_dashboard')

@login_required
def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
@teacher_required
def teacher_dashboard(request):
    if request.user.role != 'teacher':
        return HttpResponseForbidden("You are not allowed to access this page.")
    return render(request, 'accounts/teacher_dashboard.html')

@login_required
@student_required
def student_dashboard(request):
    if request.user.role != 'student':
        return HttpResponseForbidden("You are not allowed to access this page.")
    return render(request, 'accounts/student_dashboard.html')