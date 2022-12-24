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
        dealerships = get_dealers_from_cf(url)                               
        # Concat all dealer's short name
        #dealer_names = '<br>'.join([  'Dealer: ' + dealer.short_name  for dealer in dealerships])
        # Return a list of dealer short name
        #return HttpResponse(dealer_names)

        return render(request, 'djangoapp/index.html', {"dealership_list":dealerships})


   
# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...

def get_review_by_dealer(request, dealer_id, dealer_name):

    print("get_review_by_dealer---------",dealer_id, dealer_name)

    url="https://us-south.functions.appdomain.cloud/api/v1/web/6265d22b-6b9e-4c35-b6e9-8363063d5443/car-review/reviews"
    reviews = get_dealer_reviews_from_cf(url,dealer_id)
    count=len(reviews)
    return render(request, 'djangoapp/dealer_details.html', {"reviews_list":reviews,"dealer_id":dealer_id, "dealer_name":dealer_name,"count":count})


    #names = '<br>'.join([  'Review: ' + e.name +', '+ e.review for e in elements])
    # Return a list of dealer short name
    #return HttpResponse(names)
    #return JsonResponse({ 'view': 'get_review_by_dealer','id': id})



# Create a `add_review` view to submit a review
# http://127.0.0.1:8000/djangoapp/addreview/10/Alphazap%20Car%20Dealership
def add_review(request, dealer_id, dealer_name):

    # if user is authenticated 
    if request.user.is_authenticated==False:
        return redirect("djangoapp:index")


    if request.method =="GET":

        #query the locals cars with the dealer id to be reviewed
        cars = CarModel.objects.filter(dealerid=dealer_id)
        print("add_review, cars:",len(cars))

        #inject year car.year.strftime("%Y")
        
        return render(request, 'djangoapp/add_review.html', {"cars_list":cars, "dealer_id":dealer_id, "dealer_name":dealer_name})

    elif request.method == 'POST':

        
        review= request.POST["review"] 
        #print("purchasecheck" in request.POST)
        if "purchasecheck" in request.POST:
            purchase= True
        else:
            purchase= False     

        purchase_date = request.POST["purchasedate"]
        carId =request.POST["car"]
        car = CarModel.objects.get(id=carId)
        print("add_review POST------------")
        #print("     car:",carId,car.make,car.name,car.year)
        
        new_review={
            "id":  datetime.utcnow().timestamp(),
            "name": dealer_name,
            "dealership": dealer_id,
            "review": review,
            "purchase": purchase,           
            "purchase_date": purchase_date,
            "car_make": car.make.name,
            "car_model": car.name,
            "car_year": car.year.strftime("%Y"),
            "datetime": datetime.utcnow().isoformat()
                }

   

        payload={"review":new_review}
        url="https://us-south.functions.appdomain.cloud/api/v1/web/6265d22b-6b9e-4c35-b6e9-8363063d5443/car-review/reviews"

        status_code, response = post_request(url, payload)
        print("   status: ",status_code)
        if status_code != 201: #Create
            return JsonResponse(response)
    
        return redirect("djangoapp:reviews", dealer_id=dealer_id,dealer_name=dealer_name)

        #return JsonResponse({ 'view': 'add_review_to_dealer','id': id})


