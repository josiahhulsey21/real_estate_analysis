import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class ZSalesCrawlSpider(CrawlSpider):
    name = 'z_sales_crawl'
    allowed_domains = ['www.zillow.com']
    start_urls = ['https://www.zillow.com/troy-il/sold/']

    rules = (
            Rule(LinkExtractor(restrict_xpaths="//div[@class = 'list-card-top']/a"), callback='parse_item', follow=True),
    )

    def parse_item(self, response):

        yield{
            'home_description':response.xpath("//div[@class = 'zsg-content-item home-description']/div/text()").get()

        }


