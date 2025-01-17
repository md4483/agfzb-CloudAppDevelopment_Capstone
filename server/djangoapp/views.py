from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarModel
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.
# Create an `about` view to render a static about page
def about(request):
    context = {}
    return render(request, 'djangoapp/about.html', context)

# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password"
            return render(request, 'djangoapp/index.html', context)
    else:
        return render(request, 'djangoapp/index.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    context = {}
    logout(request)
    context['message'] = "Successfully logged out"
    return render(request, 'djangoapp/index.html', context)

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['password']
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
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = "https://eu-gb.functions.appdomain.cloud/api/v1/web/9e5a21cb-e2b3-457f-bc1c-064d900cb0ea/dealership-package/get-dealership"
        # Get dealers from the URL
        context['dealerships'] = get_dealers_from_cf(url)
        # Return a list of dealer short name
        return render(request, 'djangoapp/index.html', context)

# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context = {}
    url = "https://eu-gb.functions.appdomain.cloud/api/v1/web/9e5a21cb-e2b3-457f-bc1c-064d900cb0ea/dealership-package/get-dealership"
    # Get dealer from the URL
    context['dealership'] = get_dealers_from_cf(url, dealerId=dealer_id)
    
    url = "https://eu-gb.functions.appdomain.cloud/api/v1/web/9e5a21cb-e2b3-457f-bc1c-064d900cb0ea/dealership-package/get-review"
    context['reviews'] = get_dealer_reviews_from_cf(url, dealerId=dealer_id)
    # Return a list of dealer short name
    return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
def add_review(request, dealer_id):    
    context = {}
    if request.method == 'GET':
        url = "https://eu-gb.functions.appdomain.cloud/api/v1/web/9e5a21cb-e2b3-457f-bc1c-064d900cb0ea/dealership-package/get-dealership"
        cars = CarModel.objects.filter(dealer_id=dealer_id)
        context = {
            "dealer_id": dealer_id,
            "dealer_name": get_dealers_from_cf(url)[0].full_name,
            "cars": cars,
            "cur_date": datetime.today().strftime('%Y-%m-%d')
        }
        return render(request, 'djangoapp/add_review.html', context)
    
    if request.method == 'POST':
        if (request.user.is_authenticated):
            review = {}
            review['name'] = request.user.first_name + ' ' + request.user.last_name
            review['dealership'] = dealer_id
            review['review'] = request.POST['review']

            if 'purchase' in request.POST:
                review['purchase'] = True
            else:
                review['purchase'] = 'false'

            if review['purchase'] is True:
                if request.POST['car_purchased']:
                    car = request.POST['car_purchased'].split('!!')
                    review['car_make'] = car[0]
                    review['car_model'] = car[1]
                    review['car_year'] = car[2]
                else:
                    review['car_make'] = ' '
                    review['car_model'] = ' '
                    review['car_year'] = ' '

                review['purchase_date'] = request.POST['purchase_date']
            else:
                review['purchase_date'] = 'wat'
                review['car_make'] = ' '
                review['car_model'] = ' '
                review['car_year'] = ' '
            
            url = "https://eu-gb.functions.appdomain.cloud/api/v1/web/9e5a21cb-e2b3-457f-bc1c-064d900cb0ea/dealership-package/post_review"
            json_payload = review
            json_result = post_request(url, json_payload)

            if 'error' in json_result:
                context['message'] = "An error occurred submitting your review"
            else:
                context['message'] = "Review submitted successfully"
        return redirect('djangoapp:dealer_details', dealer_id=dealer_id)
