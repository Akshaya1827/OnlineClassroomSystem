from django.shortcuts import redirect

def teacher_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.role == 'teacher':
            return view_func(request, *args, **kwargs)
        return redirect('dashboard')
    return wrapper


def student_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.role == 'student':
            return view_func(request, *args, **kwargs)
        return redirect('dashboard')
    return wrapper
