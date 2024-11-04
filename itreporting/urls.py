from django.urls import path
from . import views  # Import views from the current app (itreporting)
from users import views as users_views  # Rename users views to avoid conflict

app_name = 'itreporting'

urlpatterns = [
    path('', views.home, name='home'),                  # Refers to the itreporting home view
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('report/', views.report, name='report'),
    path('register/', users_views.register, name='register'),  # Refers to the users register view
]