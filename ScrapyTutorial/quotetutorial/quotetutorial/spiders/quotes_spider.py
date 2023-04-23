import scrapy
from ..items import QuotetutorialItem

class QuoteSpider(scrapy.Spider):
    name = "quotes"

    start_urls = {
        "https://quotes.toscrape.com/"
    }

    def parse(self, response): #Here response contains the source code of quotes.toscrape.com 
        """# title = response.css('title').extract() #This will also return title tag with text.
        title = response.css('title::text').extract() #This will only return text inside title tag.
        #this yield is a keyword which is same as return keyword.
        yield {"titletxt": title}"""

        items = QuotetutorialItem() #It is the method which we use to store scraped data to the temparory container and then we can store data into database.

        #Web scraping Quotes and Authors.
        all_div_quotes = response.css("div.quote") #This will contain all the div.quote data

        for quotes in all_div_quotes:
            title = quotes.css("span.text::text").extract() #from all the data now we can extract whatever we want.
            author = quotes.css(".author::text").extract()
            tag = quotes.css(".tag::text").extract()

            items['title'] = title
            items['author'] = author
            items['tag'] = tag

            yield items
            # yield {
            #         "title": title,
            #         "author": author,
            #         "tag": tag
            #     }
