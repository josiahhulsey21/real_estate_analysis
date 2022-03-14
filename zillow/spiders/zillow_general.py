import scrapy
from datetime import datetime
import json
import http.client, urllib.parse



class ZillowGeneralSpider(scrapy.Spider):
    name = 'zillow_general'
    allowed_domains = ['www.zillow.com']
    start_urls = ['https://www.zillow.com/centralia-wa/sold']

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

        def clean_string(input_item):
            try:
                input_item = input_item.lower()
                input_item = input_item.replace('$','')
                input_item = input_item.replace(',','')  
                input_item = input_item.replace('"','')  
                
                input_item = input_item.replace('/month','')
            
            except:
                input_item = 'no value'
            return input_item

        def clean_string_convert_to_float (input_item):
            try:
            #check to see if the returned value exists. If it doesnt, replace it with 0
                if input_item == "":
                    input_item = '0'
                input_item = input_item.lower()
                input_item = input_item.replace('/month','')
                input_item = input_item.replace('studiio','1')
                input_item = input_item.replace('$','')
                input_item = input_item.replace(',','')
                input_item = float(input_item)

            except:
                input_item = '0' 
                input_item = float(input_item)                            
            return(input_item)

        def clean_string_convert_to_date (input_item):
            try:
                if input_item == "":
                    input_item = '01/01/1900'
                
                input_item = input_item.lower()
                
                input_item = input_item.replace('sold ','')

                input_item = input_item.replace(' ','')
                        
                input_item= datetime.strptime(input_item, '%m/%d/%Y').date()
            except:
                input_item = '01/01/1990'
                input_item= datetime.strptime(input_item, '%m/%d/%Y').date()


            return(input_item)

        def clean_string_convert_lot(input_item):

            try:
                input_item = input_item.lower()
                input_item = input_item.replace(',','') 
                if 'sqft' in input_item:
                    input_item = input_item.replace('sqft','')
                    input_item = float(input_item)
                    input_item = round(input_item / 43560,2)
                elif 'acres' in input_item:
                    input_item = input_item.replace('acres','')
                    input_item = float(input_item)
                elif 'acre' in input_item:
                    input_item = input_item.replace('acres','')
                    input_item = float(input_item)
                elif "â€" in input_item:
                    input_item = 0.0
                elif '—' in input_item:
                    input_item = 0.0
                elif input_item == "":
                    input_item = 0.0
                
            
            except:
                input_item = 0.0
            
            return (input_item)

        def clean_string_basic(input_item):
           if input_item =="":
               input_item = 'no value'
           else:
               input_item = input_item
            
           return(input_item)

        def geocode(address):       
                
            try:
                api = '1a26d763ab4991ad4ad1a057ab15b4df'
                conn = http.client.HTTPConnection('api.positionstack.com')

                params = urllib.parse.urlencode({
                    'access_key': api,
                    'query': address,
                    'region': 'Washington State',
                    'limit': 1,
                    })

                conn.request('GET', '/v1/forward?{}'.format(params))

                res = conn.getresponse()
                data = res.read()


                geocoded_response = data.decode('utf-8')
                # print(geocoded_response)
                gc_dict = json.loads(geocoded_response)

                latitude = gc_dict['data'][0]['latitude']
                longitude = gc_dict['data'][0]['longitude']
                confidence = gc_dict['data'][0]['confidence']
                looked_up_address = gc_dict['data'][0]['label']

            except:
                latitude = 9999999999
                longitude = 9999999999
                confidence = 0
                looked_up_address = 'failed to geocode address'        


            return [latitude, longitude, confidence, looked_up_address]



        #to call a variable from the above parse function your have to pass it the key value from the dictionary formated below
        address = response.request.meta['address']
        
        sale_price = response.request.meta['sale_price']
        sale_price = clean_string_convert_to_float(sale_price)
        
        sale_date = response.request.meta['sale_date']
        sale_date = clean_string_convert_to_date(sale_date)
        
        beds = response.request.meta['beds']
        beds = clean_string_convert_to_float(beds)

        baths = response.request.meta['baths']
        baths = clean_string_convert_to_float(baths)

        sqft = response.request.meta['sqft']
        sqft = clean_string_convert_to_float(sqft)

        link = response.request.meta['link']


        zestimate = response.xpath("//div[@class = 'zestimate-value']/text()").get()
        zestimate = clean_string_convert_to_float(zestimate)
        
        z_rent_estimate = response.xpath("(//p[@class='Text-aiai24-0 StyledParagraph-sc-18ze78a-0 bfISgk'])[1]/span/text()").get()
        z_rent_estimate = clean_string_convert_to_float(z_rent_estimate)
        
        home_desc = response.xpath("//div[@class = 'ds-overview-section']/div/text()").get()
        home_desc = clean_string_basic(home_desc)

        home_type = response.xpath("(//span[contains(text(),'Type')])[1]/following-sibling::node()/text()").get()
        home_type = clean_string_basic(home_type)
        
        year_built = response.xpath("(//span[contains(text(),'Year built:')])[1]/following-sibling::node()/text()").get()
        year_built = clean_string_convert_to_float(year_built)

        heating = response.xpath("//span[contains(text(),'Heating:')]/following-sibling::node()/text()").get()
        cooling = response.xpath("//span[contains(text(),'Cooling:')]/following-sibling::node()/text()").get()
        parking = response.xpath("//span[contains(text(),'Parking:')]/following-sibling::node()/text()").get()
        
        
        lot = response.xpath("//span[contains(text(),'Lot:')]/following-sibling::node()/text()").get()
        lot = clean_string_convert_lot(lot)
        
        
        
        
        e_school = response.xpath("//ul[@class = 'ds-nearby-schools-list']/li[1]/div/a/text()").get()
        e_school = clean_string_basic(e_school)
        e_school_rating = response.xpath("(//ul[@class = 'ds-nearby-schools-list']/li/div/div/span)[1]/text()").get()
        e_school_rating = clean_string_convert_to_float(e_school_rating)
        m_school = response.xpath("(//ul[@class = 'ds-nearby-schools-list']/li[2])/div/a/text()").get()
        m_school = clean_string_basic(m_school)
        m_school_rating = response.xpath("(//ul[@class = 'ds-nearby-schools-list']/li[2])/div/div/span[1]/text()").get()
        m_school_rating = clean_string_convert_to_float(m_school_rating)
        h_school = response.xpath("//ul[@class = 'ds-nearby-schools-list']/li[3]/div/a/text()").get()
        h_school = clean_string_basic(h_school)
        h_school_rating = response.xpath("(//ul[@class = 'ds-nearby-schools-list']/li[3])/div/div/span[1]/text()").get()
        h_school_rating = clean_string_convert_to_float(h_school_rating)


        gc_list = geocode(address)
        latitude = gc_list[0]
        longitude = gc_list[1]
        confidence = gc_list[2]
        looked_up_address = gc_list[3]
        
        
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
            'latitude':latitude,
            'longitude':longitude,
            'confidence':confidence,
            'looked_up_address':looked_up_address,
            'link':link
        }

















