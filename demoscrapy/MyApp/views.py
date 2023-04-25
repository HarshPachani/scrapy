from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

import requests
from datetime import datetime
from scrapy import Selector
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from MyApp.models import PetrolPrice
from django.db import transaction
import json

# Create your views here.
def index(request):

    even_price = []
    odd_price = []

    even_cities = []
    odd_cities = []

    # Define the URL to scrape
    url = 'https://www.goodreturns.in/petrol-price-in-gujarat-s12.html'

    # Use requests to get the HTML content of the page
    response = requests.get(url)

    # Use scrapy to parse the HTML content
    selector = Selector(text=response.text)

    # Extract the petrol price from the parsed HTML
    try:
        petrol_price_even = selector.css(
            '.gold_silver_table table .even_row td').getall()

        petrol_price_odd = selector.css(
            '.gold_silver_table table .odd_row td').getall()

        # access for the today's petrol price only
        for j in range(1, len(petrol_price_even), 3):
            selector = Selector(text=petrol_price_even[j])
            price = selector.css('td::text').get()
            even_price.append(float(price[2:]))

        for j in range(1, len(petrol_price_odd), 3):
            selector = Selector(text=petrol_price_odd[j])
            price = selector.css('td::text').get()
            odd_price.append(float(price[2:]))

        # print((even_price+odd_price))

        petrol_price = even_price+odd_price
        # print(petrol_price)
    
        for i in petrol_price_even:
            selector = Selector(text=i)
            city = selector.css('td a::attr(title)').get()
            # print("City: ", city)
            if city is None:
                pass
            else:
                # pass
                # print(f"{city} : city")
                even_cities.append(city)

        for i in petrol_price_odd:
            selector = Selector(text=i)
            city = selector.css('td a::attr(title)').get()
            if city is None:
                pass
            else:
                odd_cities.append(city)
        
        # print("Even Cities: ")
        # for city in even_cities:
        #     print(city)
    
        # print("Odd Cities: ")
        # for city in odd_cities:
        #     print(city)

        petrol_city = even_cities + odd_cities
        # print(petrol_city)

    except Exception as e:
        return HttpResponse('Failed')
    date = datetime.now()

    res = {}
    for key, value in zip(petrol_city, petrol_price):
        res[key] = value

    # print("Result: ", res)

    with open("data.json", "w") as fp:
        json.dump(res,fp, indent = 4)


    with open('data.json') as json_file:
        data = json.load(json_file)

    return JsonResponse(data)