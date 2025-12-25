from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('instructor', 'Instructor'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    bio = models.TextField(blank=True, null=True)
    device_limit = models.IntegerField(default=1) # Requirement: device limit control
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    @property
    def unread_notifications_count(self):
        return self.notifications.filter(is_read=False).count()
