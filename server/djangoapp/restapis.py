import requests
import json
# import related models here
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 \
    import Features, SentimentOptions

from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    try:
        response = requests.post(url, params=kwargs, json=json_payload)
    except Exception as e:
        print("Error", e)
    return response

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, **kwargs)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result
        # For each dealer object
        for dealer in dealers:
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                                   id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                                   short_name=dealer["short_name"],
                                   st=dealer["st"], zip=dealer["zip"])
            results.append(dealer_obj)

    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list

def get_dealer_reviews_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, **kwargs)
    if json_result:
        # Get the row list in JSON as dealers
        reviews = json_result
        # For each dealer object
        for review in reviews:
            # Create a CarDealer object with values in `doc` object
            if "purchase_date" in review:
                review_obj = DealerReview(dealership=review["dealership"], name=review["name"], 
                    purchase=review["purchase"], review=review["review"],
                    purchase_date=review["purchase_date"], car_make=review["car_make"], 
                    car_model=review["car_model"], car_year=review["car_year"])
            else:
                review_obj = DealerReview(dealership=review["dealership"], name=review["name"], 
                    purchase=review["purchase"], id=review["id"], review=review["review"], )

            review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            results.append(review_obj)

    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(text):
    url = "https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com/instances/aba8a47c-d136-4f6d-86df-1fcc29714d5b"
    api_key = "UEJToFWYT4M5g1sUipkQcUOG97jscsNIudZ8XTOQSuLT"

    authenticator = IAMAuthenticator(api_key)
    nlu = NaturalLanguageUnderstandingV1(version='2021-08-01',authenticator=authenticator)
    nlu.set_service_url(url)

    response = nlu.analyze(text=text,
                features=Features(sentiment=SentimentOptions(targets=[text])),
                language='en').get_result()
    label = response['sentiment']['document']['label'] 

    return label
