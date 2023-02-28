"""_summary_
Yields:
_type_: _description_
"""

import scrapy

class HomesSpider(scrapy.Spider):
    name = "homes"
    start_urls = ['https://www.homes.com/homes-for-sale/?bb=3qnyjrinvS__k2vnkqhH&property_type=32,1&listing_type=64,8']

    def parse(self, response, **kwargs):
        for properties in response.css('div.for-sale-content-container'):
            try:
                yield {
                    'address' : properties.css('div.for-sale-content-container a::attr(title)').get().split(',')[0],
                    'city' : properties.css('div.for-sale-content-container a::attr(title)').get().split(',')[1].strip().split(' ')[0],
                    'state' : properties.css('div.for-sale-content-container a::attr(title)').re_first(r', ([A-Z]{2}) \d{5}$'),
                    'zip' : properties.css('div.for-sale-content-container a::attr(title)').get().split()[-1],
                    'size' : properties.css('ul.detailed-info-container')[0].css('li::text').getall(),
                    'price' : properties.css('p.price-container::text').get().strip(),
                    'link' : properties.css('a').attrib['href'],
                    'agent' : properties.css('span.agent-name::text').get(),
                    'agency' : properties.css('span.agency-name::text').get()
                }
            except (IndexError, AttributeError):
                yield {
                    'address' : "not available",
                    'city' : "not available",
                    'state' : "not available",
                    'zip' : "not available",
                    'size' : "not available",
                    'price' : properties.css('p.price-container::text').get().strip(),
                    'link' : properties.css('a').attrib['href'],
                    'agent' : properties.css('span.agent-name::text').get(),
                    'agency' : properties.css('span.agency-name::text').get()
                }
                

        next_page_number = response.css('button.next.text-only').attrib.get('data-page')
        next_page = f"https://www.homes.com/homes-for-sale/p{next_page_number}/?bb=3qnyjrinvS__k2vnkqhH&property_type=32,1&listing_type=64,8"
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
