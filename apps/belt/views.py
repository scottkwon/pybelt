from django.shortcuts import render
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import render,redirect
from .models import User, Trip
import bcrypt
from datetime import datetime

# Create your views here.
def main(request):
    return render(request, 'belt/login.html')

def process(request):
    if request.method == 'POST':
        data = request.POST.copy()
        errors = User.objects.registration(data)
        if isinstance(errors, int):
            user = User.objects.get(id=errors)
            request.session['user_id'] = user.id
            request.session['username'] = user.username
            return redirect('/travels')
        for error in errors:
            messages.error(request, error)
    return redirect('/main')

def login(request):
    if request.method == 'POST':
        data = request.POST.copy()
        errors = User.objects.verify_login(data)
        if not errors:
            user = User.objects.get(username=data['username'])
            request.session['user_id'] = user.id
            request.session['username'] = user.username
            return redirect('/travels')
        for error in errors:
            messages.error(request,error)
    return redirect('/main')

def traveldash(request):
    if 'user_id' not in request.session:
        return redirect('/main')
    print request.session['user_id']
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'my_trips': Trip.objects.filter(host=user)|Trip.objects.filter(trips=user),
        'other_trips': Trip.objects.exclude(host=user).exclude(trips=user)
    }
    return render(request, 'belt/travels.html', context)


def add(request):
    if 'user_id' not in request.session:
        return redirect('/main')
    return render(request, 'belt/add.html')


def verify(request):
    data = request.POST.copy()
    user = User.objects.get(id=request.session['user_id'])
    result = Trip.objects.validate(data, user)
    if isinstance(result, list):
        for error in result:
            messages.error(request, error)
    if isinstance(result,int):
        messages.success(request,"Succesfully Added Trip!")
        return redirect('/travels/')
    return redirect(reverse('tbuddy:add'))


def destination(request, id):
    if 'user_id' not in request.session:
        return redirect('/main')
    context= {
        'trip': Trip.objects.get(id=id),
        'other_users': User.objects.filter(trip_users__id=id)
    }
    return render(request, 'belt/destination.html', context)

def join(request,id):
    user = User.objects.get(id=request.session['user_id'])
    trip = Trip.objects.get(id=id)
    trip.trips.add(user)
    return redirect('/travels')

def logout(request):
    request.session.clear()
    return redirect('/main')
