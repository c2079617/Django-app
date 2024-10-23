from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse('<h1>Student IT Services Home</h1>')

def about(request):
    return HttpResponse('<h1>About Us</h1><p>DCBS Django Jack.</p>')

def contact(request):
    return HttpResponse('<h1>Contact Us</h1><p>c2079617@hallam.shu.ac.uk</p>')
