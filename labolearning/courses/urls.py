from django.urls import path
from . import views

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('request/<int:course_id>/', views.request_enrollment, name='request_enrollment'),
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('<int:course_id>/', views.course_detail, name='course_detail'),
    path('lesson/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    path('<int:course_id>/comment/', views.add_comment, name='add_comment'),
    path('assignment/<int:assignment_id>/submit/', views.submit_assignment, name='submit_assignment'),
    path('<int:course_id>/add-lesson/', views.add_lesson, name='add_lesson'),
    path('<int:course_id>/add-assignment/', views.add_assignment, name='add_assignment'),
]
