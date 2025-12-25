from django import forms
from courses.models import Course, Lesson, Assignment, EnrollmentRequest

class EnrollmentRequestForm(forms.ModelForm):
    class Meta:
        model = EnrollmentRequest
        fields = ['phone', 'email', 'whatsapp', 'message']
        widgets = {
            'phone': forms.TextInput(attrs={'placeholder': '+1234567890'}),
            'email': forms.EmailInput(attrs={'placeholder': 'your@email.com'}),
            'whatsapp': forms.TextInput(attrs={'placeholder': 'WhatsApp Number or Link'}),
            'message': forms.Textarea(attrs={'placeholder': 'Anything else you want to tell the instructor?', 'rows': 3}),
        }
from live_sessions.models import LiveSession

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'content', 'video_file', 'order']

class LiveSessionForm(forms.ModelForm):
    class Meta:
        model = LiveSession
        fields = ['title', 'scheduled_at', 'duration_minutes']
        widgets = {
            'scheduled_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'description', 'due_date']
        widgets = {
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
