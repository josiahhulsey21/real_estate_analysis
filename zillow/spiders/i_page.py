import scrapy


class IPageSpider(scrapy.Spider):
    name = 'i_page'
    allowed_domains = ['www.zillow.com']
    # start_urls = ['https://www.zillow.com/homedetails/116-Oakland-Dr-Troy-IL-62294/65274868_zpid/']
    # start_urls = ['https://www.zillow.com/homes/23915-Hamptonshire-Ln-Katy,-TX,-77494_rb/59753186_zpid/']
    start_urls = ['https://www.zillow.com/homedetails/210-Montgomery-St-Troy-IL-62294/147860085_zpid/']
    # start_urls = ['https://www.zillow.com/homedetails/114-Sugarmill-Rd-Troy-IL-62294/4927743_zpid/']



    # start_urls = ['https://www.zillow.com/homedetails/114-Sugarmill-Rd-Troy-IL-62294/4927743_zpid/','https://www.zillow.com/homedetails/210-Montgomery-St-Troy-IL-62294/147860085_zpid/']
    





    def parse(self, response):
        # if response.css('#captchacharacters').extract_first():
        #     print('Captcha Found')

        zestimate = response.xpath("//div[@class = 'zestimate primary-quote']/div/text()[3]").get(),
        home_desc = response.xpath("//div[@class = 'zsg-content-item home-description']/div/text()").get(),
        type_residence = response.xpath("//div[@class = 'home-facts-at-a-glance-section']/div[1]/div/div[2]/text()").get(),
        year_built = response.xpath("//div[@class = 'home-facts-at-a-glance-section']/div[2]/div[2]/div[2]/text()").get(),
        lot = response.xpath("//div[@class = 'home-facts-at-a-glance-section']/div[7]/div[2]/div[2]/text()").get(),
        # parking = response.xpath("//div[@class = 'home-facts-at-a-glance-section']/div[5]/div[2]/div[2]]/text()").get(),
        last_sale_price = response.xpath("(//div[@class = 'fact-value'])[63]/text()").get(),
        # taxes = response.xpath("(//div[@class = 'fact-value'])[43]/text()/text()").get()



        cooling= response.xpath("(//div[@class = 'fact-value'])[16]/text()").get()
        # yeat_built = response.xpath("//div[@class = 'home-facts-at-a-glance-section']/div[2]/div[2]/div[2]/text()").get(),
        # yeat_built = response.xpath("//div[@class = 'home-facts-at-a-glance-section']/div[2]/div[2]/div[2]/text()").get(),
        # yeat_built = response.xpath("//div[@class = 'home-facts-at-a-glance-section']/div[2]/div[2]/div[2]/text()").get(),
        # yeat_built = response.xpath("//div[@class = 'home-facts-at-a-glance-section']/div[2]/div[2]/div[2]/text()").get(),
        # yeat_built = response.xpath("//div[@class = 'home-facts-at-a-glance-section']/div[2]/div[2]/div[2]/text()").get(),
        # yeat_built = response.xpath("//div[@class = 'home-facts-at-a-glance-section']/div[2]/div[2]/div[2]/text()").get(),




        yield{
            'home_description': home_desc,
            'type_of_residence':type_residence,
            'year_built':year_built,
            'lot':lot,
            'zest':zestimate,
            # 'parking':parking,
            'last_sale_price':last_sale_price,
            # 'taxes':taxes,
            'cooling':cooling
        }



