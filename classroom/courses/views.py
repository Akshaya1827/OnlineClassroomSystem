from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import CourseForm, JoinCourseForm, CourseMaterialForm
from .models import Course, Enrollment, CourseMaterial, MaterialFile
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.db.models import Count
@login_required
def create_course(request):
    if request.user.role != "teacher":
        return HttpResponseForbidden("Not allowed")
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
def update_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if request.user != course.teacher:
        return HttpResponseForbidden("Not allowed")

    if request.method == "POST":
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect("teacher_dashboard")
    else:
        form = CourseForm(instance=course)

    return render(request, "courses/update_course.html", {"form": form})

@login_required
def course_list(request):
    if request.user.role == "teacher":
        courses = Course.objects.filter(teacher=request.user)
    else:
        courses = Course.objects.all()

    return render(request, "courses/course_list.html", {"courses": courses})

@login_required
def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if request.user != course.teacher:
        return HttpResponseForbidden("Not allowed")

    if request.method == "POST":
        course.delete()
        return redirect("teacher_dashboard")

    return render(request, "courses/delete_course.html", {"course": course})

@login_required
def teacher_dashboard(request):
    courses = Course.objects.filter(teacher=request.user).annotate(student_count=Count("enrollment"))
    return render(request, 'accounts/teacher_dashboard.html', {'courses': courses})

@login_required
def join_course(request):
    if request.user.role != 'student':
        messages.error(request, "Only students can join courses.")
        return redirect('teacher_dashboard')

    if request.method == 'POST':
        form = JoinCourseForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['course_code']

            try:
                
                course = Course.objects.get(course_code__iexact=code)

                
                already_enrolled = Enrollment.objects.filter(
                    student=request.user,
                    course=course
                ).exists()

                if already_enrolled:
                    messages.warning(request, "You are already enrolled in this course.")
                else:
                    Enrollment.objects.create(
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
    if request.user.role != "student":
        return redirect("teacher_dashboard")

    enrollments = Enrollment.objects.filter(student=request.user)
    course_ids = enrollments.values_list("course_id", flat=True)
    courses = Course.objects.filter(id__in=course_ids)

    return render(
        request,
        "accounts/student_dashboard.html",
        {"courses": courses}
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
            files = request.FILES.getlist("files")

            for f in files:
                MaterialFile.objects.create(
                    material=material,
                    file=f
                )
            return redirect('view_materials', course_id=course.id)
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

from django.shortcuts import get_object_or_404

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    return render(request, "courses/course_detail.html", {
        "course": course
    })

@login_required
def delete_material_file(request, file_id):
    file = MaterialFile.objects.get(id=file_id)

    if request.user != file.material.course.teacher:
        messages.error(request, "Permission denied.")
        return redirect("teacher_dashboard")

    course_id = file.material.course.id

    if request.method == "POST":
        file.delete()
        return redirect("view_materials", course_id=course_id)

@login_required
def update_material_file(request, file_id):
    file = MaterialFile.objects.get(id=file_id)

    if request.user != file.material.course.teacher:
        messages.error(request, "Permission denied.")
        return redirect("teacher_dashboard")

    if request.method == "POST":
        new_file = request.FILES.get("file")
        if new_file:
            file.file = new_file
            file.save()
        return redirect("view_materials", course_id=file.material.course.id)

    return render(request, "courses/update_material_file.html", {
        "file": file
    })

