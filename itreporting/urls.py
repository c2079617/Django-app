from django.urls import path
from . import views  
from users import views as users_views 
from students import views as students_views  
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView

app_name = 'itreporting'

urlpatterns = [
    path('', views.home, name='home'),  # Views from 'itreporting' app
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('register/', users_views.register, name='register'),  # Views from 'users' app
    path('studentsregister/', students_views.studentsregister, name='studentsregister'),  # Views from 'students' app
    path('profile/', users_views.profile, name='profile'),
    path('report/', PostListView.as_view(), name='report'),
    path('issues/<int:pk>', PostDetailView.as_view(), name='issue-detail'),
    path('issue/new', PostCreateView.as_view(), name='issue-create'),
    path('issues/<int:pk>/update/', PostUpdateView.as_view(), name='issue-update'),
    path('issue/<int:pk>/delete/', PostDeleteView.as_view(), name='issue-delete'),
    path('modules/', views.modules, name='modules'),
    path('modules/<int:module_id>/', views.module_detail, name='module_detail'),
    path('modules/<int:module_id>/register/', views.register_module, name='register_module'),
    path('modules/<int:module_id>/unregister/', views.unregister_module, name='unregister_module'),
]
