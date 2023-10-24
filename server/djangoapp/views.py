from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarModel
from .restapis import get_dealers_from_cf, get_dealer_by_id_from_cf, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
from random import randrange

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.
#def get_dealerships(request):
  #  context = {}
   #if request.method == "GET":
   # url = "https://us-south.functions.appdomain.cloud/api/v1/web/f7eef718-affe-45b0-b6fc-6de4b624888f/dealership-package/get-dealership"
        # Get dealers from the URL
   # dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
   # dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
   # return HttpResponse(dealer_names)


def get_dealerships(request):
    if request.method == "GET":
        context = {}
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/f7eef718-affe-45b0-b6fc-6de4b624888f/dealership-package/get-dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        context["dealership_list"] = dealerships
        return render(request, 'djangoapp/index.html', context)


# Create an `about` view to render a static about page
def about(request):
    return render(request,'djangoapp/about.html')


# Create a `contact` view to return a static contact page
def contact(request):
    return render(request,'djangoapp/contact.html')

#def home(request):
  #  return render(request,'djangoapp/index.html' )

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    # Handles POST request
    if request.method == "POST":
        # Get username and password from request.POST dictionary
        username = request.POST['username']
        password = request.POST['psw']
        # Try to check if provide credential can be authenticated
        user = authenticate(username=username, password=password)
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)
            return redirect('djangoapp:index')
        else:
            # If not, return to login page again
            return render(request, 'djangoapp/index.html', context)
    else:
        return render(request, 'djangoapp/index.html', context)

# ...


# Create a `logout_request` view to handle sign out request
def logout_request(request):
    # Get the user object based on session id in request
    print("Log out the user `{}`".format(request.user.username))
    # Logout user in the request
    logout(request)
    # Redirect user back to course list view
    return redirect('djangoapp:index')
# ...

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    return render(request,'djangoapp/registration.html')


#user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                   # password=password)
# Update the `get_dealerships` view to render the index page with a list of dealerships
#def get_dealerships(request):
  #  context = {}
   # if request.method == "GET":
    #    return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
#def get_dealer_details(request, dealer_id):
 #   if request.method == "GET":
  #      context = {}
   #     dealer_url = "https://us-south.functions.appdomain.cloud/api/v1/web/f7eef718-affe-45b0-b6fc-6de4b624888f/dealership-package/get-dealership"
    #    dealer = get_dealer_by_id_from_cf(dealer_url, id=dealer_id)
     #   context["dealer"] = dealer
    
      #  review_url = "https://us-south.functions.appdomain.cloud/api/v1/web/f7eef718-affe-45b0-b6fc-6de4b624888f/dealership-package/get-review"
       # reviews = get_dealer_reviews_from_cf(review_url, id=dealer_id)
       # print(reviews)
       # context["reviews"] = reviews
        
        #return render(request, 'djangoapp/dealer_details.html', context)


def get_dealer_details(request, id):

    if request.method == "GET":
        context = {}
        dealer_url = "https://us-south.functions.appdomain.cloud/api/v1/web/f7eef718-affe-45b0-b6fc-6de4b624888f/dealership-package/get-dealership"
        dealer = get_dealer_by_id_from_cf(dealer_url, id=id)
        context["dealer"] = dealer

   
        review_url = "https://us-south.functions.appdomain.cloud/api/v1/web/f7eef718-affe-45b0-b6fc-6de4b624888f/dealership-package/get-review"
        reviews = get_dealer_reviews_from_cf(review_url, id=id)
        print(reviews)
        context["reviews"] = reviews

        return render(request, 'djangoapp/dealer_details.html', context)


# Create a `add_review` view to submit a review
def add_review(request, id):
    context = {}
    url = "https://us-south.functions.appdomain.cloud/api/v1/web/f7eef718-affe-45b0-b6fc-6de4b624888f/dealership-package/get-dealership"
    dealer = get_dealer_by_id_from_cf(dealer_url, id=id)
    context["dealer"] = dealer
    if request.method == 'GET':
        # Get cars for the dealer
        cars = CarModel.objects.all()
        print(cars)
        context["cars"] = cars
        
        return render(request, 'djangoapp/add_review.html', context)
    elif request.method == 'POST':
        if request.user.is_authenticated:
            username = request.user.username
            print(request.POST)
            payload = dict()
            car_id = request.POST["car"]
            car = CarModel.objects.get(pk=car_id)
            payload["time"] = datetime.utcnow().isoformat()
            payload["name"] = username
            payload["dealership"] = id
            payload["id"] = id
            payload["review"] = request.POST["content"]
            payload["purchase"] = False
            if "purchasecheck" in request.POST:
                if request.POST["purchasecheck"] == 'on':
                    payload["purchase"] = True
            payload["purchase_date"] = request.POST["purchasedate"]
            payload["car_make"] = car.make.name
            payload["car_model"] = car.name
            payload["car_year"] = int(car.year.strftime("%Y"))

            new_payload = {}
            new_payload["review"] = payload
            json_result = post_request("https://us-south.functions.appdomain.cloud/api/v1/web/f7eef718-affe-45b0-b6fc-6de4b624888f/dealership-package/post-review", new_payload, id=id)
            post_request(review_post_url, new_payload, id=id)
        return redirect("djangoapp:dealer_details", id=id)

