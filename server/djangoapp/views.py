from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarMake,CarModel
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
    return render(request, 'djangoapp/about.html')


# Create a `contact` view to return a static contact page
def contact(request):
    return render(request, 'djangoapp/contact.html')

# Create a `login_request` view to handle sign in request
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
            return render(request, 'djangoapp/user_login_bootstrap.html', context)
    else:
        return render(request, 'djangoapp/user_login_bootstrap.html', context)


# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')


# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/user_registration_bootstrap.html', context)
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
            return render(request, 'djangoapp/user_registration_bootstrap.html', context)





# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships2(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/index.html', context)

def get_dealerships(request):
    if request.method == "GET":
        #url = "your-cloud-function-domain/dealerships/dealer-get"
        url="https://us-south.functions.appdomain.cloud/api/v1/web/6265d22b-6b9e-4c35-b6e9-8363063d5443/car-review/dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url,None)                               
        # Concat all dealer's short name
        dealer_names = '<br>'.join([  'Dealer: ' + dealer.short_name  for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_names)


   
# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...

def get_review_by_dealer(request, id):

    url="https://us-south.functions.appdomain.cloud/api/v1/web/6265d22b-6b9e-4c35-b6e9-8363063d5443/car-review/reviews"
    elements = get_dealer_reviews_from_cf(url,id)
    names = '<br>'.join([  'Review: ' + e.name +', '+ e.review for e in elements])
        # Return a list of dealer short name
    return HttpResponse(names)

    #return JsonResponse({ 'view': 'get_review_by_dealer','id': id})



# Create a `add_review` view to submit a review
def add_review(request, id):

    # if user is authenticated 
    # extraer datos de un formulario ??


    review={
          "id": 1114,
          "name": "Upkar Lidder",
          "dealership": id,
          "review": "Great service!",
          "purchase": False,
          "another": "field",
          "purchase_date": "02/16/2021",
          "car_make": "Audi",
          "car_model": "Car",
          "car_year": 2021,
          "datetime": datetime.utcnow().isoformat()
            }

    payload={"review":review}
    url="https://us-south.functions.appdomain.cloud/api/v1/web/6265d22b-6b9e-4c35-b6e9-8363063d5443/car-review/reviews"

    response = post_request(url, payload)
    return JsonResponse(response)

    #return JsonResponse({ 'view': 'add_review_to_dealer','id': id})


