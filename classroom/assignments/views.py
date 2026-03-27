from importlib.resources import files
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Assignment, AssignmentFile, Submission, SubmissionFile
from .forms import AssignmentForm, SubmissionForm
from courses.models import Course
from django.utils import timezone


@login_required
def create_assignment(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if request.user.role != 'teacher':
        return redirect('student_dashboard')

    if request.method == 'POST':
        form = AssignmentForm(request.POST,request.FILES)
        
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.course = course
            assignment.save()
            files = request.FILES.getlist("files")
            for f in files:
                AssignmentFile.objects.create(
                    assignment=assignment,
                    file=f
                )

            messages.success(request, "Assignment created successfully!")
            return redirect('teacher_dashboard')
    else:
        form = AssignmentForm()

    return render(request, 'assignments/create_assignment.html', {
        'form': form,
        'course': course
    })


@login_required
def assignment_list(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    assignments = Assignment.objects.filter(course=course)

    submissions = Submission.objects.filter(
        assignment__course=course,
        student=request.user
    )

    submission_map = {}

    for sub in submissions:
        if sub.files.exists():   # ✅ check files
            submission_map[sub.assignment.id] = sub

    for assignment in assignments:
        assignment.user_submission = submission_map.get(assignment.id)

    return render(request, 'assignments/assignment_list.html', {
        'assignments': assignments,
        'course': course
    })

@login_required
def submit_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)

    if request.user.role != 'student':
        return redirect('teacher_dashboard')
    existing_submission = Submission.objects.filter(
        assignment=assignment,
        student=request.user
    ).first()
    if existing_submission and not existing_submission.files.exists():
        existing_submission = None
    is_closed = False
    if assignment.due_date and timezone.now() > assignment.due_date:
        is_closed = True

    if request.method == 'POST' and not is_closed:
        form = SubmissionForm(request.POST, request.FILES)

        if form.is_valid():

            # 🔹 Calculate score here (ONLY when submitting)
            if assignment.due_date:
                total_time = (assignment.due_date - assignment.created_at).total_seconds()
                remaining_time = (assignment.due_date - timezone.now()).total_seconds()

                if remaining_time < 0:
                    remaining_time = 0

                score = (remaining_time / total_time) * 100
            else:
                score = 100
            files = request.FILES.getlist("files")

            if not files:
                messages.error(request, "Please upload at least one file.")
                return redirect(request.path)
            if existing_submission:
                submission = existing_submission
                submission.score = round(score, 2)
                submission.save()
            else:
                submission = Submission.objects.create(
                assignment=assignment,
                student=request.user,
                score=round(score, 2)
          )

            for f in files:
                SubmissionFile.objects.create(
                submission=submission,
                file=f
        )


            messages.success(request, "Assignment submitted successfully!")
            return redirect('assignment_list', course_id=assignment.course.id)
    else:
        form = SubmissionForm()

    return render(request, 'assignments/submit_assignment.html', {
        'form': form,
        'assignment': assignment,
        'existing_submission': existing_submission,
        'is_closed': is_closed
    })

@login_required
def view_submissions(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)

    if request.user.role != 'teacher':
        return redirect('student_dashboard')

    submissions = Submission.objects.filter(assignment=assignment)
    total = submissions.count()

    return render(request, 'assignments/view_submissions.html', {
        'assignment': assignment,
        'submissions': submissions,
        'total': total
    })

@login_required
def delete_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)

    if request.user != assignment.course.teacher:
        messages.error(request, "You are not allowed to delete this assignment.")
        return redirect('teacher_dashboard')

    if request.method == "POST":
        course_id = assignment.course.id
        assignment.delete()
        messages.success(request, "Assignment deleted successfully.")
        return redirect('assignment_list', course_id=course_id)


    return render(request, 'assignments/confirm_delete_assignment.html', {
        'assignment': assignment
    })
@login_required
def update_assignment(request, assignment_id):
    assignment = Assignment.objects.get(id=assignment_id)

    if request.user != assignment.course.teacher:
        messages.error(request, "Only teacher can update assignment.")
        return redirect('teacher_dashboard')

    if request.method == "POST":
        form = AssignmentForm(request.POST, request.FILES, instance=assignment)

        if form.is_valid():
            form.save()

            # If new file uploaded, replace old file
            new_file = request.FILES.get("file")
            if new_file:
                # Delete old files
                AssignmentFile.objects.filter(assignment=assignment).delete()

                # Save new file
                AssignmentFile.objects.create(
                    assignment=assignment,
                    file=new_file
                )

            return redirect('teacher_dashboard')
    else:
        form = AssignmentForm(instance=assignment)

    return render(request, "assignments/update_assignment.html", {
        "form": form,
        "assignment": assignment
    })


@login_required
def delete_submission(request, submission_id):
    submission = Submission.objects.get(id=submission_id)
    assignment = submission.assignment

    if request.user != submission.student:
        messages.error(request, "Permission denied.")
        return redirect("student_dashboard")

    if assignment.due_date and timezone.now() > assignment.due_date:
        messages.error(request, "Cannot delete after due date.")
        return redirect("assignment_list", course_id=assignment.course.id)

    if request.method == "POST":
        submission.delete()

    return redirect("assignment_list", course_id=assignment.course.id)

@login_required
def update_submission(request, submission_id):
    submission = Submission.objects.get(id=submission_id)
    assignment = submission.assignment

    if request.user != submission.student:
        messages.error(request, "Permission denied.")
        return redirect("student_dashboard")

    if assignment.due_date and timezone.now() > assignment.due_date:
        messages.error(request, "Cannot update after due date.")
        return redirect("assignment_list", course_id=assignment.course.id)

    if request.method == "POST":
        files = request.FILES.getlist("files")

        for f in files:
            SubmissionFile.objects.create(
                submission=submission,
                file=f
            )

        return redirect("assignment_list", course_id=assignment.course.id)

    return render(request, "assignments/update_submission.html", {
        "submission": submission
    })

@login_required
def delete_submission_file(request, file_id):
    file = get_object_or_404(SubmissionFile, id=file_id)
    submission = file.submission

    if request.user != submission.student:
        messages.error(request, "Permission denied.")
        return redirect("student_dashboard")

    if request.method == "POST":
        file.delete()

        # 🔥 If no files left → delete submission
        if not submission.files.exists():
            submission.delete()

    return redirect("assignment_list", course_id=submission.assignment.course.id)