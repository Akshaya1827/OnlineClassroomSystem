from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CourseForm, JoinCourseForm, CourseMaterialForm
from .models import Course, Enrollment, CourseMaterial
from django.contrib import messages

@login_required
def create_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.teacher = request.user
            course.save()
            return redirect('teacher_dashboard')
    else:
        form = CourseForm()

    return render(request, 'courses/create_course.html', {'form': form})

@login_required
def teacher_dashboard(request):
    courses = Course.objects.filter(teacher=request.user)
    return render(request, 'accounts/teacher_dashboard.html', {'courses': courses})

@login_required
def join_course(request):
    # only students can join
    if request.user.role != 'student':
        messages.error(request, "Only students can join courses.")
        return redirect('student_dashboard')

    if request.method == 'POST':
        form = JoinCourseForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['course_code']

            try:
                course = Course.objects.get(course_code=code)
                Enrollment.objects.get_or_create(
                    student=request.user,
                    course=course
                )
                messages.success(request, "Successfully enrolled in course!")
                return redirect('student_dashboard')

            except Course.DoesNotExist:
                messages.error(request, "Invalid course code.")

    else:
        form = JoinCourseForm()

    return render(request, 'courses/join_course.html', {'form': form})

@login_required
def student_dashboard(request):
    enrollments = Enrollment.objects.filter(student=request.user)
    return render(
        request,
        'accounts/student_dashboard.html',
        {'enrollments': enrollments}
    )


@login_required
def upload_material(request, course_id):
    course = Course.objects.get(id=course_id)

    if request.user != course.teacher:
        messages.error(request, "Only teacher can upload materials.")
        return redirect('teacher_dashboard')

    if request.method == 'POST':
        form = CourseMaterialForm(request.POST, request.FILES)
        if form.is_valid():
            material = form.save(commit=False)
            material.course = course
            material.save()
            return redirect('teacher_dashboard')
    else:
        form = CourseMaterialForm()

    return render(request, 'courses/upload_material.html', {'form': form, 'course': course})


@login_required
def view_materials(request, course_id):
    course = Course.objects.get(id=course_id)
    materials = course.materials.all()
    return render(request, 'courses/view_materials.html', {
        'course': course,
        'materials': materials
    })
