from django.urls import path
from . import views  # Import views from the current app (itreporting)
from users import views as users_views  # Import views from users app with alias
from .views import PostListView, PostDetailView, PostCreateView

app_name = 'itreporting'

urlpatterns = [
    path('', views.home, name='home'),                  # Refers to the itreporting home view
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('reportus/', views.reportus, name='reportus'),
    path('register/', users_views.register, name='register'),  # Refers to the users register view
    path('profile/', users_views.profile, name='profile'),  # Refers to the users profile view
    path('report/', PostListView.as_view(), name = 'report'),
    path('issues/<int:pk>', PostDetailView.as_view(), name = 'issue-detail'),
    path('issue/new', PostCreateView.as_view(), name = 'issue-create'),
]