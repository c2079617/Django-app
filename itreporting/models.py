from django.db import models
from django.utils.timezone import now
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
    date_submitted = models.DateTimeField(default=now)
    author = models.ForeignKey(User, related_name='issues', on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.type} Issue in {self.room}'

    def get_absolute_url(self):
        return reverse('itreporting:issue-detail', kwargs={'pk': self.pk})
    
class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.title

class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default='pending')
    enrolled_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} enrolled in {self.course.title}"