from django.urls import path
from . import views  
from users import views as users_views 
from students import views as students_views  
from .views import (
    PostListView, 
    PostDetailView, 
    PostCreateView, 
    PostUpdateView, 
    PostDeleteView,
    courses_list,
    course_detail,
    enroll_course, 
    dashboard,
)

app_name = 'itreporting'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('success/', views.success, name='success'),

    
    path('register/', users_views.register, name='register'),
    path('studentsregister/', students_views.studentsregister, name='studentsregister'),
    path('profile/', users_views.profile, name='profile'),
    path('change_password/', users_views.change_password, name='change_password'),


    path('report/', PostListView.as_view(), name='report'),
    path('issues/<int:pk>/', PostDetailView.as_view(), name='issue-detail'),
    path('issue/new/', PostCreateView.as_view(), name='issue-create'),
    path('issues/<int:pk>/update/', PostUpdateView.as_view(), name='issue-update'),
    path('issue/<int:pk>/delete/', PostDeleteView.as_view(), name='issue-delete'),

 
    path('courses/', views.courses_list, name='courses_list'),
    path('courses/<int:pk>/', views.course_detail, name='course_detail'),
    path('courses/<int:pk>/enroll/', views.enroll_course, name='enroll_course'),
    path('courses/<int:pk>/unenroll/', views.unenroll_course, name='unenroll_course'),
    path('dashboard/', views.dashboard, name='dashboard'),
]