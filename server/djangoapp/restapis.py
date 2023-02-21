import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions

def get_request(url, **kwargs):
    try:
        response = requests.get(url, headers={'Content-Type': 'application/json'}, params=kwargs)
    except:
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

def post_request(url, payload, **kwargs):
    response = requests.post(url, params=kwargs, json=payload)
    return response

def get_dealers_from_cf(url, **kwargs):
    results = []
    json_result = get_request(url)
    if json_result:
        dealers = json_result["result"]
        for dealer in dealers:
            dealer_doc = dealer["doc"]
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"], id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"], short_name=dealer_doc["short_name"], st=dealer_doc["st"], zip=dealer_doc["zip"],state=dealer_doc["state"])
            results.append(dealer_obj)
    return results

def get_dealers_by_id_cf(url):
    results = []
    json_result = get_request(url)
    if json_result:
        dealers = json_result["result"]["docs"]
        for key in dealers:
            key_item = CarDealer(address=key["address"], city=key["city"], full_name=key["full_name"], id=key["id"], lat=key["lat"], long=key["long"], short_name=key["short_name"], st=key["st"], zip=key["zip"], state=key["state"])
            results.append(key_item)
    return results

def get_dealer_review(url):
    results = []
    json_result = get_request(url)
    if json_result:
        reviews = json_result["docs"]
        for key in reviews:
            if key["purchase"] == False:
                key["purchase_date"] = " "
                key["car_make"] = " "
                key["car_model"] = " "
                key["car_year"] = " "
            review_item = DealerReview(dealership=key["dealership"], name=key["name"], purchase=key["purchase"], review=key["review"], purchase_date=key["purchase_date"], car_make=key["car_make"], car_model=key["car_model"], car_year=key["car_year"], sentiment=analyze_review_sentiments(key["review"]), id="2")
            results.append(review_item)
    return results

def analyze_review_sentiments(review_text):
    # hardcoded in as not a PROD environment
    url = 'https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com/instances/01c7d2d9-e63f-474c-b9cc-6efc84fe0240'
    api_key = 'fqJ8oW-3dHSyqaZN01yNzp4VmWx8kWO--80nUVkJGtWy'
    version = '2021-08-01'
    authenticator = IAMAuthenticator(api_key)
    nlu = NaturalLanguageUnderstandingV1(version=version, authenticator=authenticator)
    nlu.set_service_url(url)
    response = nlu.analyze(text=review_text, features=Features(sentiment=SentimentOptions())).get_result()
    sentiment_label = response["sentiment"]["document"]["label"]
    return sentiment_label
