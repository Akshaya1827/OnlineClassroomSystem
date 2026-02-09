from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from .models import User
from django.contrib.auth.decorators import login_required
from .decorators import teacher_required,student_required
def register(request):
    if request.method == 'POST':
        User.objects.create_user(
            username=request.POST['email'],
            email=request.POST['email'],
            password=request.POST['password'],
            role=request.POST['role']
        )
        return redirect('login')
    return render(request, 'accounts/register.html')
# Create your views here.
def user_login(request):
    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST['email'],
            password=request.POST['password']
        )
        if user:
            login(request, user)
            return redirect('dashboard')  # temporary redirect
    return render(request, 'accounts/login.html')


@login_required
def dashboard(request):
    if request.user.role == 'teacher':
        return redirect('teacher_dashboard')
    return redirect('student_dashboard')


def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
@teacher_required
def teacher_dashboard(request):
    return render(request, 'accounts/teacher_dashboard.html')

@login_required
@student_required
def student_dashboard(request):
    return render(request, 'accounts/student_dashboard.html')