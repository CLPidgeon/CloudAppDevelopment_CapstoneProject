from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.models import User
from .models import CarModel
from django.shortcuts import get_object_or_404, render, redirect
from .restapis import get_dealers_from_cf, get_dealers_by_id_cf, get_dealer_review
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)
BASE_URL = "https://us-south.functions.appdomain.cloud/api/v1/web/b8bcfb3d-03eb-4f5e-89cf-a9acfc6ddf07/dealership-package"

# Create an `about` view to render a static about page
def about(request):
    return render(request, 'djangoapp/about.html')

# Create a `contact` view to return a static contact page
def contact(request):
    return render(request, 'djangoapp/contact.html')

def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/index.html', context)
    else:
        return render(request, 'djangoapp/index.html', context)

def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration', context)

def get_dealerships(request):
    if request.method == "GET":
        context = {}
        url = BASE_URL + "/get-dealership.json"
        dealerships = get_dealers_from_cf(url)
        context['dealerships_list'] = dealerships
        return render(request, 'djangoapp/index.html', context)

def get_dealerships_by_id(request, dealer_id):
    if request.method == "GET":
        if (int(dealer_id)):
            url = BASE_URL + "/get-dealership.json?dealerId=" + dealer_id
        else:
            url = BASE_URL + "/get-dealership.json?state=" + dealer_id
        dealerships = get_dealers_by_id_cf(url)
        review_url = BASE_URL + "/get-review.json?dealerId=" + str(dealer_id)
        context = {}
        reviews = get_dealer_review(review_url)
        context['reviews_list'] = reviews
        context['dealer'] = dealerships[0]
        return render(request, 'djangoapp/dealer_details.html', context)

def review(request, dealer_id):
    context = {}
    if request.method == 'GET':
        url = BASE_URL + "/get-dealership.json?dealerId=" + dealer_id
        dealerships = get_dealers_by_id_cf(url)
        cars = CarModel.objects.filter(dealer_id=dealer_id)
        context['dealer'] = dealerships[0]
        context['cars'] = cars
        return render(request, 'djangoapp/add_review.html', context)
    elif request.method == 'POST':
        url = BASE_URL + "/post-review.json?"   
        return redirect("djangoapp:dealer_details", dealer_id=dealer_id)