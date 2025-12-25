from django.shortcuts import render, redirect

def home(request):
    return render(request, 'index.html')

def login_success(request):
    if request.user.role == 'instructor' or request.user.is_staff:
        return redirect('instructor_dashboard')
    return redirect('student_dashboard')
