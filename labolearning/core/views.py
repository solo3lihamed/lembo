from django.shortcuts import render, redirect
from courses.models import Course

def home(request):
    if request.user.is_authenticated:
        if request.user.role == 'instructor' or request.user.is_staff:
            return redirect('instructor_dashboard')
        return redirect('student_dashboard')
    
    featured_courses = Course.objects.all()[:3]
    return render(request, 'index.html', {'featured_courses': featured_courses})

def login_success(request):
    if request.user.role == 'instructor' or request.user.is_staff:
        return redirect('instructor_dashboard')
    return redirect('student_dashboard')
