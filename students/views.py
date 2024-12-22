from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm

def studentsregister(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('itreporting:home')
        else:
            messages.warning(request, 'Unable to create account.')
    else:
        form = UserRegisterForm()
        return render(request, 'students/register.html', {'form': form, 'title': 'StudentRegistration'})