from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, 'main_app/index.html')

def register(request):
    if request.method == 'POST':
        print request.POST
        response_from_models = User.objects.add_user(request.POST)
        # if failed validations
        if not response_from_models['status']:
            for error in response_from_models['errors']:
                messages.error(request, error)
            return redirect('users:index')
        # if true on validations
        else:
            request.session['user_id'] = response_from_models['user'].id
            return redirect('users:success')
    else:
        return redirect('users:index')

def login(request):
    response_from_models = User.objects.check_user(request.POST)
    if not response_from_models['status']:
        for error in response_from_models['errors']:
            messages.error(request, error)
        return redirect('users:index')
    else:
        request.session['user_id'] = response_from_models['user_id']
        return redirect('users:success')

def success(request):
    if not 'user_id' in request.session:
        messages.error(request, 'Must be logged in!')
        return redirect('users:index')
    return render(request, 'main_app/success.html')

def logout(request):
    request.session.clear()
    return redirect('users:index')
