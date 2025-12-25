from django.contrib import admin
from .models import Course, Lesson, EnrollmentRequest, Enrollment
from notifications.models import Notification

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor', 'created_at')
    search_fields = ('title', 'instructor__username')

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')
    list_filter = ('course',)

@admin.register(EnrollmentRequest)
class EnrollmentRequestAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'status', 'requested_at', 'phone', 'email', 'whatsapp', 'message_snippet')
    list_filter = ('status', 'course')
    search_fields = ('student__username', 'course__title', 'message')
    actions = ['approve_requests', 'reject_requests']
    readonly_fields = ('requested_at', 'student', 'course', 'phone', 'email', 'whatsapp', 'message')

    def message_snippet(self, obj):
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    message_snippet.short_description = 'Message'

    def approve_requests(self, request, queryset):
        for obj in queryset:
            if obj.status == 'pending':
                # Create enrollment
                Enrollment.objects.get_or_create(student=obj.student, course=obj.course)
                # Update request
                obj.status = 'approved'
                obj.save()
                # Notify student
                Notification.objects.create(
                    user=obj.student,
                    message=f"Your request for '{obj.course.title}' has been approved! 🎉",
                    link=f"/courses/dashboard/"
                )
        self.message_user(request, "Selected requests have been approved.")
    approve_requests.short_description = "Approve selected enrollment requests"

    def reject_requests(self, request, queryset):
        queryset.update(status='rejected')
        for obj in queryset:
            Notification.objects.create(
                user=obj.student,
                message=f"Sorry, your request for '{obj.course.title}' was rejected. 😔"
            )
        self.message_user(request, "Selected requests have been rejected.")

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'enrolled_at')
