from django.contrib import admin
from .models import Issue, Course, Module, Student

admin.site.register(Issue)
admin.site.register(Course)
admin.site.register(Module)
admin.site.register(Student)