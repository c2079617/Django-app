from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Issue, Course, Enrollment
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
import requests
from django.contrib.auth.decorators import login_required
from .forms import ContactForm
from django.core.mail import EmailMessage

def home(request):
    weather_url = 'https://api.openweathermap.org/data/2.5/weather?q={},{}&units=metric&appid={}'
    cities = [('Sheffield', 'UK'), ('Melaka', 'Malaysia'), ('Bandung', 'Indonesia')]
    weather_data = []
    weather_api_key = '053ef24e299f9acb9b9fb5e27f16ef88'

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

    news_api_key = '303cbe99d8634e23aa430e2a67eef806'
    news_url = 'https://newsapi.org/v2/top-headlines'
    news_params = {
        'apiKey': news_api_key,
        'country': 'us',
        'category': 'technology',
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
        'articles': articles,
    }

    return render(request, 'itreporting/home.html', context)

def about(request):
    context = {
        'google_maps_api_key': 'AIzaSyCPDLwe-PbX5TH_LDA9KC9nELLycZj8ZB4',
        'latitude': 53.3787,
        'longitude': -1.4652
    }

    return render(request, 'itreporting/about.html', context)

def contact(request):
    return render(request, 'itreporting/contact.html')

def report(request):
    daily_report = {'issues': Issue.objects.all(), 'title': 'Issues Reported'}
    return render(request, 'itreporting/report.html', daily_report)

class PostListView(ListView):
    model = Issue
    ordering = ['-date_submitted']
    template_name = 'itreporting/report.html'
    context_object_name = 'issues'
    paginate_by = 4

class PostDetailView(DetailView):
    model = Issue
    template_name = 'itreporting/issue_detail.html'

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Issue
    fields = ['type', 'room', 'urgent', 'details']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Issue
    fields = ['type', 'room', 'details']

    def test_func(self):
        issue = self.get_object()
        return self.request.user == issue.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Issue
    success_url = '/report'

    def test_func(self):
        issue = self.get_object()
        return self.request.user == issue.author

def courses_list(request):
    courses = Course.objects.all()
    return render(request, 'itreporting/courses_list.html', {'courses': courses})

def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    return render(request, 'itreporting/course_detail.html', {'course': course})

@login_required
def enroll_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    Enrollment.objects.get_or_create(user=request.user, course=course)
    return redirect('itreporting:dashboard')

@login_required
def dashboard(request):
    enrollments = Enrollment.objects.filter(user=request.user)
    return render(request, 'itreporting/dashboard.html', {'enrollments': enrollments})

@login_required
def unenroll_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    enrollment = Enrollment.objects.filter(user=request.user, course=course).first()

    if enrollment:
        enrollment.delete()

    return redirect('itreporting:dashboard')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            subject = form.cleaned_data['subject']
            room = form.cleaned_data['room']
            message = form.cleaned_data['message']

            email_body = f"""
            Name: {name}
            Email: {email}
            Phone: {phone}
            Subject: {subject}
            Room: {room}

            Message:
            {message}
            """

            email_message = EmailMessage(
                f'Contact Form Submission from {name}',
                email_body,
                email,
                ['DjangoTestmail@gmail.com'],
                reply_to=[email]
            )

            try:
                email_message.send(fail_silently=False)
                return redirect('itreporting:success')
            except Exception as e:
                print(f"Error sending email: {e}")
                return HttpResponse("Error sending email. Please try again.")
    else:
        form = ContactForm()

    return render(request, 'itreporting/contact.html', {'form': form})

def success(request):
    return render(request, 'itreporting/success.html')