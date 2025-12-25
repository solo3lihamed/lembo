from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Course, EnrollmentRequest, Enrollment, Lesson, LessonProgress, Assignment, AssignmentSubmission, CourseComment
from .forms import LessonForm, AssignmentForm
from django.contrib import messages
from notifications.models import Notification
from django.utils import timezone

def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses/course_list.html', {'courses': courses})

@login_required
def request_enrollment(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if Enrollment.objects.filter(student=request.user, course=course).exists():
        messages.info(request, "You are already enrolled!")
        return redirect('student_dashboard')
    
    if EnrollmentRequest.objects.filter(student=request.user, course=course, status='pending').exists():
        messages.info(request, "Request already pending.")
        return redirect('course_list')
    
    EnrollmentRequest.objects.create(student=request.user, course=course)
    messages.success(request, f"Request sent for '{course.title}'! 🚀")
    return redirect('course_list')

@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    is_enrolled = Enrollment.objects.filter(student=request.user, course=course).exists()
    is_instructor = course.instructor == request.user or request.user.is_staff
    
    if not (is_enrolled or is_instructor):
        messages.error(request, "You must be enrolled to view this course! 😠")
        return redirect('course_list')
    
    lessons = course.lessons.all()
    assignments = course.assignments.all()
    comments = course.comments.all().order_by('-created_at')
    
    return render(request, 'courses/course_detail.html', {
        'course': course,
        'lessons': lessons,
        'assignments': assignments,
        'comments': comments,
        'is_instructor': is_instructor
    })

@login_required
def lesson_detail(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    course = lesson.course
    is_enrolled = Enrollment.objects.filter(student=request.user, course=course).exists()
    is_instructor = course.instructor == request.user or request.user.is_staff

    if not (is_enrolled or is_instructor):
        messages.error(request, "Access denied. 🛑")
        return redirect('course_list')

    # Mark as completed/progress
    progress, created = LessonProgress.objects.get_or_create(student=request.user, lesson=lesson)
    if not progress.is_completed:
        progress.is_completed = True
        progress.completed_at = timezone.now()
        progress.save()

    return render(request, 'courses/lesson_detail.html', {
        'lesson': lesson,
        'course': course,
        'is_instructor': is_instructor
    })

@login_required
def add_comment(request, course_id):
    if request.method == 'POST':
        course = get_object_or_404(Course, id=course_id)
        text = request.POST.get('text')
        if text:
            CourseComment.objects.create(course=course, user=request.user, text=text)
            messages.success(request, "Comment posted! 🤡")
    return redirect('course_detail', course_id=course_id)

@login_required
def submit_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    if request.method == 'POST' and request.FILES.get('file'):
        AssignmentSubmission.objects.create(
            assignment=assignment,
            student=request.user,
            file=request.FILES['file']
        )
        messages.success(request, "Assignment submitted! Hope you did your best. 🏆")
    return redirect('course_detail', course_id=assignment.course.id)

@login_required
def add_lesson(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if course.instructor != request.user and not request.user.is_staff:
        return redirect('home')
    
    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.course = course
            lesson.save()
            messages.success(request, "Lesson added! 🎪")
            return redirect('course_detail', course_id=course.id)
    else:
        form = LessonForm()
    
    return render(request, 'courses/form.html', {'form': form, 'title': f'Add Lesson for {course.title}'})

@login_required
def add_assignment(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if course.instructor != request.user and not request.user.is_staff:
        return redirect('home')
    
    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.course = course
            assignment.save()
            messages.success(request, "Assignment created! 📝")
            return redirect('course_detail', course_id=course.id)
    else:
        form = AssignmentForm()
    
    return render(request, 'courses/form.html', {'form': form, 'title': f'Add Assignment for {course.title}'})

@login_required
def student_dashboard(request):
    enrollments = Enrollment.objects.filter(student=request.user)
    requests = EnrollmentRequest.objects.filter(student=request.user)
    notifications = request.user.notifications.all()[:10]
    return render(request, 'courses/dashboard.html', {
        'enrollments': enrollments,
        'requests': requests,
        'notifications': notifications
    })
