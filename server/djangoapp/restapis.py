import requests
import json
# import related models here
#from .models import CarDealer "original"
#from models import CarDealer
from requests.auth import HTTPBasicAuth


class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name

class DealerReview:

    def __init__(self, id, name, dealership, review, purchase, purchase_date, car_make, car_model, car_year,sentiment):
        
        self.id= id
        self.name = name
        self.dealership =dealership
        self.review     =review
        self.purchase   =purchase
        self.purchase_date=purchase_date
        self.car_make   =car_make
        self.car_model  =car_model
        self.car_year   =car_year
        self.sentiment  =sentiment 
    
    def __str__(self):
        return "Review: " + self.name +" :"+ self.review 
        




# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))


def get_request0(url, params):    
    print("GET from {} ".format(url))
    print(" arg:",params)
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'application/json'},params=params)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


def get_request(url,**kwargs):
    params = kwargs.get("params")
    #print("params:",params)
    if "apikey" in kwargs:
        apikey = kwargs["apikey"]
        #print("auth")
        # Basic authentication GET
        response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', apikey))        
    else:
        # No authentication GET    
        #print("No Auth")
        try:
            # Call get method of requests library with URL and parameters
            response = requests.get(url, headers={'Content-Type': 'application/json'},params=params)
        except:
            # If any error occurs
            print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data        



# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
#       requests.post(url, headers={'Content-Type': 'application/json'}, data={key: value}, json={key: value}, args) 

def post_request(url, payload):
    
    print("POST to {} ".format(url))
    #print("   payload:",payload)
    #print("   payload dump:",json.dumps(payload).encode(encoding='UTF-8',errors='strict'))
    try:
        # Call get method of requests library with URL and parameters
        
        #response = requests.post(url, headers={'Content-Type': 'application/json'},json=json.dumps(payload).encode(encoding='UTF-8',errors='strict'))
        response = requests.post(url, json=payload) # se setea solo 'Content-Type': 'application/json'
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("   status: {} ".format(status_code))
    #print("Response.content:",response.content)
    #return status_code ??
    json_data = json.loads(response.content)
    return status_code, json_data
    # 201 Created
    # 204 No Content





# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list

def get_dealers_from_cf(url, params=None):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url,params=params )
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["dealerships"] #rows
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer #["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)
    #print("length:",len(results))
    return results


# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list


def get_dealer_by_id_from_cf(url, id):
    
    return get_dealers_from_cf(url,{'id':id})[0]  

def get_dealers_by_state_from_cf(url, state): #='Kansas'   

    return get_dealers_from_cf(url,{'state':state})


# ------------------------------------------------------



# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function

def get_dealer_reviews_from_cf(url, id):

    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url,params={'dealerId':id} )
    if json_result:
        # Get the row list in JSON as dealers
        elements = json_result["reviews"] #rows
        # For each dealer object
        for e in elements:           
            
            # Create a  object from values 
            obj = DealerReview(id=e["id"], name=e["name"],
             dealership=e["dealership"], review=e["review"], 
             purchase=e["purchase"], purchase_date=e["purchase_date"], 
             car_make=e["car_make"], car_model=e["car_model"], car_year=e["car_year"],
             sentiment = analyze_review_sentiments(e["review"])
             )
            
            results.append(obj)
    # print("length:",len(results))
    return results




# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative

def analyze_review_sentiments(text):
    apikey="rDkhd9lLQtsCBVzEdK1Z3eGs63rc0PC15YRY-iz-J30A"
    url="https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/6770ddb0-6fd4-4f96-9241-69273c320661"
    url=url+"/v1/analyze"

    #'features':'keywords'
    params= {'text':text,'version':'2022-04-07','return_analyzed_text': True,'features':'sentiment','keywords.sentiment':True}

    response = get_request(url,params=params,apikey=apikey)
    print("NLU:",response)

    if "error" in response:
        label="neutral" #response['error']
    else:    
        label = response['sentiment']['document']['label']    

    print("label:",label) 
    return label








    





def reviewsTest():

    url="https://us-south.functions.appdomain.cloud/api/v1/web/6265d22b-6b9e-4c35-b6e9-8363063d5443/car-review/reviews"
    elements = get_dealer_reviews_from_cf(url,15)
    for e in elements:
        print(e)

   

def dealershipsTest():
    url="https://us-south.functions.appdomain.cloud/api/v1/web/6265d22b-6b9e-4c35-b6e9-8363063d5443/car-review/dealership"
    # Get All
    dealerships = get_dealers_from_cf(url)
    for d in dealerships:
        print(d)
    # By Id
    print("byId:",get_dealer_by_id_from_cf(url, 5))       
    # By State    
    dealerships = get_dealers_by_state_from_cf(url,'Kansas') 
    for d in dealerships:
        print(d)



def post_review():
    new_review=  {'review': {
                'id': 1671895461.533842, 
                'name': 'Alphazap Car Dealership', 
                'dealership': 15, 
                'review': 'Excellent car service and best customer attention   ', 
                'purchase': True, 
                'purchase_date':
                '11/15/2022', 
                'car_make': 'Ford', 
                'car_model': 'F 150',
                'car_year': '2020', 
                'datetime': '2022-12-24T15:24:21.535222'}}
    #payload={"review":new_review}
    url="https://us-south.functions.appdomain.cloud/api/v1/web/6265d22b-6b9e-4c35-b6e9-8363063d5443/car-review/reviews"

    response = post_request(url, new_review)
    print(response)


if __name__ == "__main__":

    #reviewsTest()
    #get_request("url",apikey="22", params={'id':1})
    #analyze_review_sentiments("Have a nice day")
    #dealershipsTest()
    #reviewsTest()
    post_review()
