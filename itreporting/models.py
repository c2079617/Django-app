from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class Issue(models.Model):
    ISSUE_TYPE_CHOICES = [
        ('Hardware', 'Hardware'),
        ('Software', 'Software'),
    ]
    
    type = models.CharField(max_length=100, choices=ISSUE_TYPE_CHOICES)
    room = models.CharField(max_length=100)
    urgent = models.BooleanField(default=False)
    details = models.TextField()
    date_submitted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, related_name='issues', on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.type} Issue in {self.room}'

    def get_absolute_url(self):
        return reverse('itreporting:issue-detail', kwargs={'pk': self.pk})
    
    
class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class Module(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50)
    credit = models.IntegerField()
    category = models.CharField(max_length=100)
    description = models.TextField()
    availability = models.BooleanField(default=True)
    allowed_courses = models.ManyToManyField(Course, related_name="modules")

    def __str__(self):
        return self.name

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    registered_modules = models.ManyToManyField(Module, related_name="students")

    def __str__(self):
        return self.user.username
