import scrapy


class DbPipelineSpider(scrapy.Spider):
    name = 'db_pipeline'
    allowed_domains = ['www.zillow.com']
    start_urls = ['https://www.zillow.com/pasadena-tx']

    def parse(self, response):
        listings= response.xpath("//ul[@class='photo-cards photo-cards_wow photo-cards_short']/li")
                
        # def geocode(address):       
                
        #     try:
        #         api = '1a26d763ab4991ad4ad1a057ab15b4df'
        #         conn = http.client.HTTPConnection('api.positionstack.com')

        #         params = urllib.parse.urlencode({
        #             'access_key': api,
        #             'query': address,
        #             'region': 'Texas',
        #             'limit': 1,
        #             })

        #         conn.request('GET', '/v1/forward?{}'.format(params))

        #         res = conn.getresponse()
        #         data = res.read()


        #         geocoded_response = data.decode('utf-8')
        #         # print(geocoded_response)
        #         gc_dict = json.loads(geocoded_response)

        #         latitude = gc_dict['data'][0]['latitude']
        #         longitude = gc_dict['data'][0]['longitude']
        #         confidence = gc_dict['data'][0]['confidence']
        #         looked_up_address = gc_dict['data'][0]['label']

        #     except:
        #         latitude = 9999999999
        #         longitude = 9999999999
        #         confidence = 0
        #         looked_up_address = 'failed to geocode address'        


        #     return [latitude, longitude, confidence, looked_up_address]        
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

        # def clean_string_convert_to_date (input_item):
        #     try:
        #         if input_item == "":
        #             input_item = '01/01/1900'
                
        #         input_item = input_item.lower()
                
        #         input_item = input_item.replace('sold ','')

        #         input_item = input_item.replace(' ','')
                        
        #         input_item= datetime.strptime(input_item, '%m/%d/%Y').date()
        #     except:
        #         input_item = '01/01/1990'
        #         input_item= datetime.strptime(input_item, '%m/%d/%Y').date()


        #     return(input_item)

        # def clean_string_convert_lot(input_item):

        #     try:
        #         input_item = input_item.lower()
        #         input_item = input_item.replace(',','') 
        #         if 'sqft' in input_item:
        #             input_item = input_item.replace('sqft','')
        #             input_item = float(input_item)
        #             input_item = round(input_item / 43560,2)
        #         elif 'acres' in input_item:
        #             input_item = input_item.replace('acres','')
        #             input_item = float(input_item)
        #         elif 'acre' in input_item:
        #             input_item = input_item.replace('acres','')
        #             input_item = float(input_item)
        #         elif "â€" in input_item:
        #             input_item = 0.0
        #         elif '—' in input_item:
        #             input_item = 0.0
        #         elif input_item == "":
        #             input_item = 0.0
                
            
        #     except:
        #         input_item = 0.0
            
        #     return (input_item)

        def clean_string_basic(input_item):
           if input_item =="":
               input_item = 'no value'
           else:
               input_item = input_item
            
           return(input_item)
    
               
        
        for listing in listings:
            try:
                
                
                asking_price = listing.xpath(".//div[@class='list-card-price']/text()").get()
                asking_price = clean_string_convert_to_float(asking_price)

                address=listing.xpath(".//address[@class='list-card-addr']/text()").get()
                address = clean_string_basic(address)
                
                
                beds=listing.xpath(".//ul[@class = 'list-card-details']/li[1]/text()").get()
                beds = clean_string_convert_to_float(beds)

                baths=listing.xpath(".//ul[@class = 'list-card-details']/li[2]/text()").get()
                baths = clean_string_convert_to_float(baths)

                sqft=listing.xpath(".//ul[@class = 'list-card-details']/li[3]/text()").get()
                sqft = clean_string_convert_to_float(sqft)

                realtor = listing.xpath(".//div[@class = 'list-card-brokerage list-card-img-overlay']/div/text()").get()
                realtor = clean_string_basic(realtor)


                whos_selling = listing.xpath(".//div[@class = 'list-card-type']/text()").get()
                realtor = clean_string_basic(realtor)

                doz = listing.xpath(".//div[@class = 'list-card-top']/div/text()").get()
                doz = clean_string_basic(doz)
                
                
                zillow_link_fa=listing.xpath(".//div[@class = 'list-card-top']/a/@href").get()
                zillow_link = listing.xpath(".//div[@class = 'list-card-top']/a/@href").get()


                # gc_list = geocode(address)
                # latitude = gc_list[0]
                # longitude = gc_list[1]
                # confidence = gc_list[2]
                # looked_up_address = gc_list[3]


                yield{
                    'asking_price':asking_price,
                    'address':address,
                    'beds':beds,
                    'baths':baths,
                    'sqft':sqft,
                    'whos_selling':whos_selling,
                    'realtor':realtor,
                    'day_on_zillow':doz,
                    # 'latitude':latitude,
                    # 'longitude':longitude,
                    # 'confidence':confidence,
                    # 'looked_up_address':looked_up_address,
                    'link':zillow_link_fa
                    }
            except:
                print('failed to process, probably was an add')
                next



        # next_page_rel = response.xpath("//a[@rel='next']/@href").get()
        # next_page = response.urljoin(next_page_rel)
        
        # if next_page:
        #     yield scrapy.Request(url=next_page, callback=self.parse)