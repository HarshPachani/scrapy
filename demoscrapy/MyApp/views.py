from django.shortcuts import render
from django.http import HttpResponse

import requests
from datetime import datetime
from scrapy import Selector
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from MyApp.models import PetrolPrice
from django.db import transaction
# import sqlite3
import json


# Create your views here.
def index(request):

    petrol_price_even_ = []
    petrol_price_odd_ = []

    cities_even_ = []
    cities_odd_ = []

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
            petrol_price_even_.append(float(price[2:]))
            # print(f'{price[2:]}')

        for j in range(1, len(petrol_price_odd), 3):
            selector = Selector(text=petrol_price_odd[j])
            price = selector.css('td::text').get()
            petrol_price_odd_.append(float(price[2:]))
            # print(f'{price[2:]}')

        print((petrol_price_even_+petrol_price_odd_))

        petrol_price = petrol_price_even_+petrol_price_odd_
        print(petrol_price)
        
        # print(petrol_price_even)

        for i in petrol_price_even:
            selector = Selector(text=i)
            city = selector.css('td a::attr(title)').get()
            # price = selector.css('td::text').get()[1]
            print("City: ", city)
            if city is None:
                pass
            else:
                # pass
                print(f"{city} : city")
                cities_even_.append(city)
                # print(f"{price} : Price")

        for i in petrol_price_odd:
            selector = Selector(text=i)
            city = selector.css('td a::attr(title)').get()
            # print("City: ", city)
            if city is None:
                pass
            else:
                cities_odd_.append(city)
        
        print("Even Cities: ")
        for city in cities_even_:
            print(city)
    
        print("Odd Cities: ")
        for city in cities_odd_:
            print(city)

        petrol_city = cities_even_ + cities_odd_
        print(petrol_city)



    except Exception as e:
        return HttpResponse('Failed')
    date = datetime.now()

    res = {}
    for key in petrol_city:
        for value in petrol_price:
            res[key] = value
            petrol_price.remove(value)
            break

    with open("data.json", "w") as fp:
        json.dump(res,fp, indent = 4)

    return HttpResponse(f"Petrol{petrol_city}, price{petrol_price} ")
    # return (result)


# =====css selector for today petrol price for even rows===

# petrol_price = selector.css(
    # '.gold_silver_table table .even_row td').getall()[1]