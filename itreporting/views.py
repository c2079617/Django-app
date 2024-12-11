from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Issue
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
import requests

# Home View with Weather API integration
def home(request):
    url = 'https://api.openweathermap.org/data/2.5/weather?q={},{}&units=metric&appid={}'
    cities = [('Sheffield', 'UK'), ('Melaka', 'Malaysia'), ('Bandung', 'Indonesia')]
    weather_data = []
    api_key = '053ef24e299f9acb9b9fb5e27f16ef88'  # Use your OpenWeatherMap API key

    for city in cities:
        city_weather = requests.get(url.format(city[0], city[1], api_key)).json()

        weather = {
            'city': f"{city_weather['name']}, {city_weather['sys']['country']}",
            'temperature': city_weather['main']['temp'],
            'description': city_weather['weather'][0]['description']
        }
        weather_data.append(weather)

    return render(request, 'itreporting/home.html', {'title': 'Homepage', 'weather_data': weather_data})

# About Page
def about(request):
    return render(request, 'itreporting/about.html')

# Contact Page
def contact(request):
    return render(request, 'itreporting/contact.html')

# Assignment Features Page
def assignment_features(request):
    return render(request, 'itreporting/assignment_features.html')

# Report Page with Issue Data
def report(request):
    daily_report = {'issues': Issue.objects.all(), 'title': 'Issues Reported'}
    return render(request, 'itreporting/report.html', daily_report)

# List View for Issues
class PostListView(ListView):
    model = Issue
    ordering = ['-date_submitted']
    template_name = 'itreporting/report.html'
    context_object_name = 'issues'
    paginate_by = 4

# Detail View for an Issue
class PostDetailView(DetailView):
    model = Issue
    template_name = 'itreporting/issue_detail.html'

# Create View for Issues
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Issue
    fields = ['type', 'room', 'urgent', 'details']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

# Update View for Issues
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Issue
    fields = ['type', 'room', 'details']

    def test_func(self):
        issue = self.get_object()
        return self.request.user == issue.author

# Delete View for Issues
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Issue
    success_url = '/report'

    def test_func(self):
        issue = self.get_object()
        return self.request.user == issue.author