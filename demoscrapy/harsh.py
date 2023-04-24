from django.shortcuts import render
from django.http import HttpResponse

import requests
from datetime import datetime
from scrapy import Selector
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from MyApp.models import PetrolPrice
from django.db import transaction


# Create your views here.
def index(request):

    petrol_price_even_ = []
    petrol_price_odd_ = []
    # Define the URL to scrape
    url = 'https://www.goodreturns.in/petrol-price-in-gujarat-s12.html'

    # Use requests to get the HTML content of the page
    response = requests.get(url)

    # Use scrapy to parse the HTML content
    selector = Selector(text=response.text)

    price_odd = []
    price_even = []

    # Extract the petrol price from the parsed HTML
    try:
        petrol_price_even = selector.css(
            '.gold_silver_table table .even_row td').getall()

        petrol_price_odd = selector.css(
            '.gold_silver_table table .odd_row td').getall()

        print("\t\t\tHere")
        # access for the today's petrol price only
        for j in range(1, len(petrol_price_even), 3):
            selector = Selector(text=petrol_price_even[j])
            price = selector.css('td::text').get()
            petrol_price_even_.append(float(price[2:]))
            print(f'{price[2:]}')
            price_even.append(price[2:])

        for j in range(1, len(petrol_price_odd), 3):
            selector = Selector(text=petrol_price_odd[j])
            price = selector.css('td::text').get()
            petrol_price_odd_.append(float(price[2:]))
            print(f'odd Price: {price[2:]}')
            price_odd.append(price[2:]) 

        print("Price odd: ", price_odd)
        print("Price even: ", price_even)

        prices = price_odd + price_even
        print("All over price: ", prices)
        
        # print((petrol_price_even_+petrol_price_odd_))
        print("Even: ", petrol_price_even_)
        print()
        print("Odd: ", petrol_price_odd_)
        petrol_price = petrol_price_even+petrol_price_odd

        # print(petrol_price)

        for i in petrol_price:
            selector = Selector(text=i)
            city = selector.css('td a::attr(title)').get()
            price = selector.css('td::text').get()[1]
            if city is None:
                # pass
                print(f"{city} : city")
                print(f"{price} : Price")
            else:
                # pass
                print(f"{city} : city")
                print(f"{price} : Price")

    except Exception as e:
        return HttpResponse(f"Failed{e}")
    date = datetime.now()

    return HttpResponse(f"Petrol")


# =====css selector for today petrol price for even rows===

# petrol_price = selector.css(
    # '.gold_silver_table table .even_row td').getall()[1]
