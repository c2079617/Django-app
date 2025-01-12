from django.contrib import admin
from .models import Issue, Course, Enrollment

admin.site.register(Issue)


admin.site.register(Course)
admin.site.register(Enrollment)