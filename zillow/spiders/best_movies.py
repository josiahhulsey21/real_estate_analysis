import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BestMoviesSpider(CrawlSpider):
    name = 'best_movies'
    allowed_domains = ['imdb.com']
    #REACVITAE IF YOU DONT USE THE START_REQUEST METHOD
    start_urls = ['https://www.imdb.com/search/title/?groups=top_250&sort=user_rating']

    # user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'

    #no callback method needed here
    # def start_requests(self):
    #     yield scrapy.Request(url='Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36', headers = {
    #         'User-Agent': self.user_agent
    #     })


#if you are feeding it more than 1 xpath expressino you have to put the () back around it. Look at the default template. it should show you
    rules = (
        #use these if you mess with user agent in settings or leave default
        Rule(LinkExtractor(restrict_xpaths="//h3[@class='lister-item-header']/a"), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths= "(//a[@class='lister-page-next next-page'])[2]"),follow=True)
        # #use these if you want to use the start requests
        # Rule(LinkExtractor(restrict_xpaths="//h3[@class='lister-item-header']/a"), callback='parse_item', follow=True,process_request = 'set_user_agent'),
        # Rule(LinkExtractor(restrict_xpaths= "(//a[@class='lister-page-next next-page'])[2]"),follow=True)
    )
    # this function will feed the requests "user_agent call".ONLY NEED THIS IS YOU USE START REQUESTS
    # def set_user_agent(self, request, response):
    #     request.headers['User-Agent'] = self.user_agent
    #     return request



    def parse_item(self, response):
        #prints out the responses you get from the website
        #print(response.url)

        yield {
            'movie_title' : response.xpath("//div[@class = 'title_wrapper']/h1/text()").get(),
            'year' : response.xpath("//div[@class = 'title_wrapper']/h1/span/a/text()").get(),
            #the normalize space removes extraneous spaces and /n
            'duration' : response.xpath("normalize-space(//div[@class = 'subtext']/time/text())").get(),
            'genre' : response.xpath("//div[@class = 'subtext']/a[1]/text()").get(),
            'rating' : response.xpath("//div[@class = 'ratingValue']/strong/span/text()").get(),
            'url' : response.url
            #throw this in if you want to return the user agent to make sure your requests have proper user agent
            # 'user-agent':response.request.headers['User-Agent']              
        }


#to fix the \xao at the end of the movie title, you have to set the feed exporter to utf 8 like before. Did not do it for this. Good to note though