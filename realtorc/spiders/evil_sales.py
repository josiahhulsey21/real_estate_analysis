import scrapy
from scrapy_splash import SplashRequest
import numpy as np

class EvilSalesSpider(scrapy.Spider):
    name = 'evil_sales'
    allowed_domains = ['www.realtor.com']
    
    
    
    # start_urls = ['https://www.realtor.com/soldhomeprices/Evansville_IN','https://www.realtor.com/soldhomeprices/Evansville_IN','https://www.realtor.com/soldhomeprices/Evansville_IN/pg-3','https://www.realtor.com/soldhomeprices/Evansville_IN/pg-15','https://www.realtor.com/soldhomeprices/Evansville_IN/pg-50']
    
    base_url = 'https://www.realtor.com/soldhomeprices/Evansville_IN'
    blank_list = []
    for num in np.arange(1,51,1):
        blank_list.append(f'{base_url}/pg-{num}')
    start_urls = blank_list 


    def parse(self, response):
        
        listings = response.xpath("//ul[@class = 'srp-list-marginless list-unstyled prop-list']/li")
          

        for listing in listings:
            yield{
                'beds':listing.xpath(".//li[@data-label = 'property-meta-beds']/span/text()").get(),
                'baths':listing.xpath(".//li[@data-label = 'property-meta-baths']/span/text()").get(),
                'sqft':listing.xpath(".//li[@data-label = 'property-meta-sqft']/span/text()").get(),
                'lot':listing.xpath(".//li[@data-label = 'property-meta-lotsize']/span[1]/text()").get(),
                'lot_size_units':listing.xpath(".//li[@data-label = 'property-meta-lotsize']/span[2]/text()").get(),
                'sale_price':listing.xpath(".//div[@data-label = 'property-price']/span/text()").get(),
                'sale_date':listing.xpath(".//span[@data-label = 'property-label-sold']/span/text()").get(),
                'address':listing.xpath("normalize-space(.//span[@class = 'listing-street-address']/text())").get(),
                'city':listing.xpath(".//span[@class = 'listing-city']/text()").get(),
                'state':listing.xpath(".//span[@class = 'listing-region']/text()").get(),
                'zipcode':listing.xpath(".//span[@class = 'listing-postal']/text()").get()
            }


        # next_page_rel = response.xpath("//a[@title = 'Go to next page']/@href").get()
        # next_page_rel = response.xpath("//span[@class = 'page'][3]/a/@href").get()
        # next_page_rel = response.xpath("//span[@class = 'page'][1]/a/@href").get()
        # next_page = response.urljoin(next_page_rel)
        # print(next_page)

        
        # if next_page:
        #     yield scrapy.Request(url=next_page, callback=self.parse,dont_filter = True)




















    # nxt_page_script ='''
    # function main(splash, args)
    # splash.private_mode_enabled = False 
    # assert(splash:go(args.url))
    # assert(splash:wait(0.5))
  
    # nxt_but = splash:select("#ResultsPerPageBottom > nav > span.next > a > i")
    # nxt_but:mouse_click()
    
    # assert(splash:wait(1.0))
  
    # return {
    #    html = splash:html()

    # }
    # end
    # '''
