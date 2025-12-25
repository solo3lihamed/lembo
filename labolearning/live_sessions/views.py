from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from courses.models import Course, EnrollmentRequest
from .models import LiveSession, Attendance
from courses.forms import LiveSessionForm
from django.contrib import messages
from django.utils import timezone
from notifications.models import Notification
from django import forms

@login_required
def instructor_dashboard(request):
    if request.user.role != 'instructor' and not request.user.is_staff:
        return redirect('home')
    
    courses = Course.objects.filter(instructor=request.user)
    upcoming_sessions = LiveSession.objects.filter(course__instructor=request.user, scheduled_at__gte=timezone.now())
    pending_requests = EnrollmentRequest.objects.filter(course__instructor=request.user, status='pending')
    
    return render(request, 'live_sessions/instructor_dashboard.html', {
        'courses': courses,
        'upcoming_sessions': upcoming_sessions,
        'pending_requests': pending_requests
    })

@login_required
def live_session_detail(request, session_id):
    session = get_object_or_404(LiveSession, id=session_id)
    # Check if student is enrolled or user is instructor
    is_instructor = session.course.instructor == request.user
    is_enrolled = session.course.enrollments.filter(student=request.user).exists()
    
    if not (is_instructor or is_enrolled or request.user.is_staff):
        messages.error(request, "Access denied! Get enrolled first. 😠")
        return redirect('course_list')
    
    return render(request, 'live_sessions/session_room.html', {
        'session': session,
        'is_instructor': is_instructor
    })

@login_required
def add_live_session(request):
    if request.user.role != 'instructor' and not request.user.is_staff:
        return redirect('home')
    
    if request.method == 'POST':
        form = LiveSessionForm(request.POST)
        if form.is_valid():
            session = form.save()
            messages.success(request, "Live session scheduled! 🎥")
            # Notify Students
            for enrollment in session.course.enrollments.all():
                Notification.objects.create(
                    user=enrollment.student,
                    message=f"New Live Session: '{session.title}' scheduled for {session.scheduled_at.strftime('%Y-%m-%d %H:%M')}",
                    link=f"/live/session/{session.id}/"
                )
            return redirect('instructor_dashboard')
    else:
        form = LiveSessionForm()
        # Filter courses to only those taught by this instructor
        form.fields['course'] = forms.ModelChoiceField(queryset=Course.objects.filter(instructor=request.user))
        
    return render(request, 'courses/form.html', {'form': form, 'title': 'Schedule Live Session'})
