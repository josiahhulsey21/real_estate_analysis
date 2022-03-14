import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class EvSalesCrawlSpider(CrawlSpider):
    name = 'ev_sales_crawl'
    allowed_domains = ['www.zillow.com']
    start_urls = ['https://www.zillow.com/evansville-in/sold/']

    rules = (
            Rule(LinkExtractor(restrict_xpaths="//div[@class = 'list-card-top']/a"), callback='parse_item', follow=True),
    )

    def parse_item(self, response):

        yield{

            'bedrooms' : response.xpath("(//span[@class = 'ds-bed-bath-living-area'])[1]/span[1]/text()").get(),
            'bathrooms' : response.xpath("(//span[@class = 'ds-bed-bath-living-area'])[2]/span[1]/text()").get(),
            'sqft' : response.xpath("(//span[@class = 'ds-bed-bath-living-area'])[3]/span[1]/text()").get(),




            'home_type' : response.xpath("(//span[@class='ds-body ds-home-fact-value'])[1]/text()").get(),
            'year_build' : response.xpath("(//span[@class='ds-body ds-home-fact-value'])[2]/text()").get(),
            'heating' : response.xpath("(//span[@class='ds-body ds-home-fact-value'])[3]/text()").get(),
            'cooling' : response.xpath("(//span[@class='ds-body ds-home-fact-value'])[4]/text()").get(),
            'parking' : response.xpath("(//span[@class='ds-body ds-home-fact-value'])[5]/text()").get(),
            'lot_size' : response.xpath("(//span[@class='ds-body ds-home-fact-value'])[6]/text()").get(),
            
            
            
            
            
            'elementary_school' : response.xpath("(//span[@class='ds-school-value ds-body-small'])[1]/text()").get(),
            'elementary_school_rating' : response.xpath("(//ul[@class='ds-nearby-schools-list']/li/div/div/span)[1]/text()").get(),
            'middle_school' : response.xpath("(//span[@class='ds-school-value ds-body-small'])[2]/text()").get(),
            'middle_school_rating' : response.xpath("(//ul[@class='ds-nearby-schools-list']/li/div/div/span)[2]/text()").get(),
            'high_school' : response.xpath("(//span[@class='ds-school-value ds-body-small'])[13]/text()").get(),
            'high_school_rating' : response.xpath("(//ul[@class='ds-nearby-schools-list']/li/div/div/span)[3]/text()").get(),
            
            
            'rent_estimate' : response.xpath("(//span[@class = 'Text-aiai24-0 egyxfz'])[2]/text()").get()


            






            # 'home_description':response.xpath("//div[@class = 'zsg-content-item home-description']/div/text()").get()

        }
