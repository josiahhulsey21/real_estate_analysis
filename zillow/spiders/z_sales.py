import scrapy


class ZSalesSpider(scrapy.Spider):
    name = 'z_sales'
    allowed_domains = ['www.zillow.com']
    start_urls = ['https://www.zillow.com/troy-il/sold/']

    def parse(self, response):
        listings = response.xpath("//ul[@class='photo-cards photo-cards_wow photo-cards_short']/li")




        for listing in listings:
            yield{
                'address':listing.xpath(".//address[@class='list-card-addr']/text()").get(),
                'sale_price':listing.xpath(".//div[@class='list-card-price']/text()").get(),
                'sale_date':listing.xpath(".//div[@class='list-card-variable-text list-card-img-overlay']/text()").get(),
                'beds':listing.xpath(".//ul[@class = 'list-card-details']/li[1]/text()").get(),
                'baths':listing.xpath(".//ul[@class = 'list-card-details']/li[2]/text()").get(),
                'sqft':listing.xpath(".//ul[@class = 'list-card-details']/li[3]/text()").get(),
                'zillow_link':listing.xpath(".//div[@class = 'list-card-top']/a/@href").get()
     

            }


        next_page_rel = response.xpath("//a[@rel='next']/@href").get()
        next_page = response.urljoin(next_page_rel)

        
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)

