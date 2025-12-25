from django.urls import path
from . import views

urlpatterns = [
    path('instructor/', views.instructor_dashboard, name='instructor_dashboard'),
    path('session/<int:session_id>/', views.live_session_detail, name='session_detail'),
    path('create/', views.add_live_session, name='add_live_session'),
]
