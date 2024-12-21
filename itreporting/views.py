from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Issue, Module, Student
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
import requests
from django.contrib.auth.decorators import login_required

# Home View with Weather and News API integration
def home(request):
    # Weather API integration
    weather_url = 'https://api.openweathermap.org/data/2.5/weather?q={},{}&units=metric&appid={}'
    cities = [('Sheffield', 'UK'), ('Melaka', 'Malaysia'), ('Bandung', 'Indonesia')]
    weather_data = []
    weather_api_key = '053ef24e299f9acb9b9fb5e27f16ef88'  # OpenWeatherMap API key

    for city in cities:
        try:
            response = requests.get(weather_url.format(city[0], city[1], weather_api_key))
            response.raise_for_status()
            city_weather = response.json()
            weather = {
                'city': f"{city_weather.get('name', 'Unknown')}, {city_weather.get('sys', {}).get('country', 'Unknown')}",
                'temperature': city_weather.get('main', {}).get('temp', 'N/A'),
                'description': city_weather.get('weather', [{}])[0].get('description', 'N/A'),
            }
            weather_data.append(weather)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather data: {e}")

    # NewsAPI integration
    news_api_key = '303cbe99d8634e23aa430e2a67eef806'  # NewsAPI key
    news_url = 'https://newsapi.org/v2/top-headlines'
    news_params = {
        'apiKey': news_api_key,
        'country': 'us',  # or any other country
        'category': 'technology',  # You can change to another category if needed
    }

    try:
        news_response = requests.get(news_url, params=news_params)
        news_response.raise_for_status()
        news_data = news_response.json()
        articles = news_data.get("articles", [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching news data: {e}")
        articles = []

    context = {
        'title': 'Homepage',
        'weather_data': weather_data,
        'articles': articles,  # Add news articles to context
    }

    return render(request, 'itreporting/home.html', context)


# About Page
def about(request):

    context = {
        'google_maps_api_key': 'AIzaSyCPDLwe-PbX5TH_LDA9KC9nELLycZj8ZB4',
        'latitude': 53.3787,  # Example coordinates (London)
        'longitude': -1.4652
    }

    return render(request, 'itreporting/about.html', context)


# Contact Page
def contact(request):
    return render(request, 'itreporting/contact.html')


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
    

def modules(request):
    modules = Module.objects.all()
    return render(request, 'itreporting/modules.html', {'modules': modules})

def module_detail(request, module_id):
    module = get_object_or_404(Module, id=module_id)
    return render(request, 'itreporting/module_detail.html', {'module': module})

@login_required
def register_module(request, module_id):
    module = get_object_or_404(Module, id=module_id)
    student = request.user.student
    if module.availability and module not in student.registered_modules.all():
        student.registered_modules.add(module)
    return redirect('itreporting/module_detail', module_id=module_id)

@login_required
def unregister_module(request, module_id):
    module = get_object_or_404(Module, id=module_id)
    student = request.user.student
    if module in student.registered_modules.all():
        student.registered_modules.remove(module)
    return redirect('itreporting/module_detail', module_id=module_id)
