import scrapy


class EvSalesSpider(scrapy.Spider):
    name = 'ev_sales'
    allowed_domains = ['www.zillow.com']
    start_urls = ['https://www.zillow.com/evansville-in/sold']

    def parse(self, response):
        listings= response.xpath("//ul[@class='photo-cards photo-cards_wow photo-cards_short']/li")
        
        for listing in listings:
            try:
                sale_price = response.xpath(".//div[@class='list-card-price']/text()").get()
                address=listing.xpath(".//address[@class='list-card-addr']/text()").get()
                sale_price=listing.xpath(".//div[@class='list-card-price']/text()").get()
                sale_date=listing.xpath(".//div[@class='list-card-variable-text list-card-img-overlay']/text()").get()
                beds=listing.xpath(".//ul[@class = 'list-card-details']/li[1]/text()").get()
                baths=listing.xpath(".//ul[@class = 'list-card-details']/li[2]/text()").get()
                sqft=listing.xpath(".//ul[@class = 'list-card-details']/li[3]/text()").get()
                zillow_link_fa=listing.xpath(".//div[@class = 'list-card-top']/a/@href").get()
                zillow_link = listing.xpath(".//div[@class = 'list-card-top']/a/@href").get()

                yield response.follow(url = zillow_link, callback = self.parse_listing, meta={'sale_price':sale_price,
                'address':address,
                'sale_date':sale_date,
                'beds':beds,
                'baths':baths,
                'sqft':sqft,
                'link':zillow_link_fa})
            except:
                print('failed to process, probably was an add')
                next



        next_page_rel = response.xpath("//a[@rel='next']/@href").get()
        next_page = response.urljoin(next_page_rel)

        
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)



    def parse_listing(self, response):

        #to call a variable from the above parse function your have to pass it the key value from the dictionary formated below
        address = response.request.meta['address']
        sale_price = response.request.meta['sale_price']
        sale_date = response.request.meta['sale_date']
        beds = response.request.meta['beds']
        baths = response.request.meta['baths']
        sqft = response.request.meta['sqft']
        link = response.request.meta['link']


        zestimate = response.xpath("//div[@class = 'zestimate-value']/text()").get(),
        z_rent_estimate = response.xpath("(//p[@class='Text-aiai24-0 StyledParagraph-sc-18ze78a-0 dYSVeq'])[1]/span/text()").get(),
        home_desc = response.xpath("//div[@class = 'ds-overview-section']/div/text()").get(),
        home_type = response.xpath("(//span[contains(text(),'Type')])[1]/text()").get(),
        year_built = response.xpath("(//span[contains(text(),'Year built:')])[1]/following-sibling::node()/text()").get(),
        heating = response.xpath("//span[contains(text(),'Heating:')]/following-sibling::node()/text()").get(),
        cooling = response.xpath("//span[contains(text(),'Cooling:')]/following-sibling::node()/text()").get(),
        parking = response.xpath("//span[contains(text(),'Parking:')]/following-sibling::node()/text()").get(),
        lot = response.xpath("//span[contains(text(),'Lot:')]/following-sibling::node()/text()").get(),
        e_school = response.xpath("//ul[@class = 'ds-nearby-schools-list']/li[1]/div/a/text()").get()
        e_school_rating = response.xpath("(//ul[@class = 'ds-nearby-schools-list']/li/div/div/span)[1]/text()").get()
        m_school = response.xpath("(//ul[@class = 'ds-nearby-schools-list']/li[2])/div/a/text()").get()
        m_school_rating = response.xpath("(//ul[@class = 'ds-nearby-schools-list']/li/div/div/span)[2]/text()").get()
        h_school = response.xpath("//ul[@class = 'ds-nearby-schools-list']/li[3]/div/a/text()").get()
        h_school_rating = response.xpath("(//ul[@class = 'ds-nearby-schools-list']/li/div/div/span)[3]/text()").get()


        yield{
            'address':address,
            'sale_price':sale_price,
            'sale_date':sale_date,
            'beds':beds,
            'baths':baths,
            'sqft':sqft,
            'year_built':year_built,
            'home_type':home_type,
            'lot_size':lot,
            'parking':parking,
            'heating':heating,
            'cooling':cooling,
            'elementary_school_rating':e_school_rating,
            'middle_school_rating':m_school_rating,
            'high_school_rating':h_school_rating,
            'elementary_school':e_school,
            'middle_school':m_school,
            'high_school':h_school,
            'zest':zestimate,
            'z_rent_estimate':z_rent_estimate,
            'home_description':home_desc,
            'link':link
        }























