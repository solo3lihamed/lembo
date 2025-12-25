import datetime
from django.core.management.base import BaseCommand
from django.utils import timezone
from users.models import User
from courses.models import Course, Lesson, EnrollmentRequest, Enrollment, Assignment, CourseComment
from live_sessions.models import LiveSession
from notifications.models import Notification

class Command(BaseCommand):
    help = 'Seeds the database with fun data for LaboLearning platform'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data... 🚀')

        # 1. Create Users
        admin, _ = User.objects.get_or_create(username='admin', defaults={'email': 'admin@labo.com', 'role': 'admin'})
        admin.set_password('adminPass123')
        admin.is_staff = True
        admin.is_superuser = True
        admin.save()

        inst1, _ = User.objects.get_or_create(username='prof_funny', defaults={'email': 'prof@labo.com', 'role': 'instructor', 'bio': 'Expert in Memeology'})
        inst1.set_password('pass123')
        inst1.save()

        inst2, _ = User.objects.get_or_create(username='creative_mind', defaults={'email': 'creative@labo.com', 'role': 'instructor', 'bio': 'Neo-Brutalism Pioneer'})
        inst2.set_password('pass123')
        inst2.save()

        stu1, _ = User.objects.get_or_create(username='student_joey', defaults={'email': 'joey@labo.com', 'role': 'student'})
        stu1.set_password('pass123')
        stu1.save()

        stu2, _ = User.objects.get_or_create(username='learning_lisa', defaults={'email': 'lisa@labo.com', 'role': 'student'})
        stu2.set_password('pass123')
        stu2.save()

        # 2. Create Courses
        c1, _ = Course.objects.get_or_create(
            title='Python for Pranksters',
            defaults={'description': 'Learn Python by building automated prank bots.', 'instructor': inst1}
        )

        c2, _ = Course.objects.get_or_create(
            title='Ugly is the New Sexy',
            defaults={'description': 'Mastering Neo-Brutalism design principles.', 'instructor': inst2}
        )

        # 3. Create Lessons
        Lesson.objects.get_or_create(course=c1, title='Setting up your Mischief Environment', defaults={'content': 'Install Python and hide your IP.', 'order': 1})
        Lesson.objects.get_or_create(course=c1, title='The Hello Prank', defaults={'content': 'Making windows pop up with funny messages.', 'order': 2})
        
        Lesson.objects.get_or_create(course=c2, title='Why Borders Matter', defaults={'content': 'Double the width, double the fun.', 'order': 1})

        # 4. Create Assignments
        Assignment.objects.get_or_create(
            course=c1, 
            title='Build a Fake Virus', 
            defaults={'description': 'Create a script that opens 100 tabs of Rick Astley.', 'due_date': timezone.now() + datetime.timedelta(days=7)}
        )

        # 5. Enrollments & Requests
        Enrollment.objects.get_or_create(student=stu1, course=c1)
        EnrollmentRequest.objects.get_or_create(student=stu2, course=c1, defaults={'status': 'pending'})
        EnrollmentRequest.objects.get_or_create(student=stu1, course=c2, defaults={'status': 'approved'})
        Enrollment.objects.get_or_create(student=stu1, course=c2)

        # 6. Live Sessions
        LiveSession.objects.get_or_create(
            course=c1, 
            title='Live Coding: The Ultimate Troll Bot', 
            defaults={'scheduled_at': timezone.now() + datetime.timedelta(hours=1), 'duration_minutes': 90, 'is_live': True}
        )

        # 7. Notifications
        Notification.objects.create(
            user=stu1,
            message="Prof Funny scheduled a new live session: 'The Ultimate Troll Bot'! Be there or be square. 🤡",
            link="/live/session/1/"
        )
        Notification.objects.create(
            user=stu2,
            message="Your request to join 'Python for Pranksters' is being reviewed. Patience is a virtue! ⏳"
        )

        # 8. Comments
        CourseComment.objects.create(course=c1, user=stu1, text="This course is legendary! My brother is so annoyed already. 😂")

        self.stdout.write(self.style.SUCCESS('Database seeded successfully! Stay funny! 🤡🤘'))
