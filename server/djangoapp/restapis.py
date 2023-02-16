import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth

def get_request(url, **kwargs):
    try:
        #if api_key:
         #   response = request.get(url, params=kwargs, auth=HTTPBasicAuth('apikey', api_key))
        #else:
        response = requests.get(url, headers={'Content-Type': 'application/json'}, params=kwargs)
    except:
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

def get_dealers_from_cf(url, **kwargs):
    results = []
    json_result = get_request(url)
    if json_result:
        dealers = json_result["result"]
        for dealer in dealers:
            dealer_doc = dealer["doc"]
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"], id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"], short_name=dealer_doc["short_name"], st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)
    return results

def get_dealers_by_id_cf(url):
    results = []
    json_result = get_request(url)
    if json_result:
        dealers = json_result["result"]["docs"]
        for key in dealers:
            key_item = CarDealer(address=key["address"], city=key["city"], full_name=key["full_name"], id=key["id"], lat=key["lat"], long=key["long"], short_name=key["short_name"], st=key["st"], zip=key["zip"])
            results.append(key_item)
    return results

def get_dealer_review(url):
    results = []
    json_result = get_request(url)
    if json_result:
        reviews = json_result["docs"]
        for key in reviews:
            review_item = DealerReview(dealership=key["dealership"], name=key["name"], purchase=key["purchase"], review=key["review"], purchase_date=key["purchase_date"], car_make=key["car_make"], car_model=key["car_model"], car_year=key["car_year"], sentiment="empty", id="2")
            results.append(review_item)
    return results

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
