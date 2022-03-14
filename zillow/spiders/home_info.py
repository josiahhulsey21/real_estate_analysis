import scrapy
import pandas as pd




class HomeInfoSpider(scrapy.Spider):
    name = 'home_info'
    allowed_domains = ['www.zillow.com']

    # link_csv = r'C:\Users\josia\OneDrive\Documents\real_estate\centralia\links_4_scrapy.csv'
    link_csv = r'C:\Users\josia\OneDrive\Documents\real_estate\centralia\links_4_scrapy_test.csv'


    df = pd.read_csv(link_csv)
    start_urls = list(df.link)

    # start_urls = ['https://www.zillow.com/homes/2296 SALZER VALLEY RD-Centralia,-WA,-98531_rb/','https://www.zillow.com/homes/408 REINKE RD-Centralia,-WA,-98531_rb/']

    def parse(self, response):


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
                        
                #you deactivated this when you hooked up to the sqlite db. Sqlite does not allow for a unique date/time to be stored.
                #this will make generating the keys to the db much easier. You will have to have a command that switched the dates
                #from strings to dates in your pandas workflow.
                # input_item= datetime.strptime(input_item, '%m/%d/%Y').date()
            except:
                input_item = '01/01/1990'
                # input_item= datetime.strptime(input_item, '%m/%d/%Y').date()


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



        try:
            beds = response.xpath("(//div[@class = 'ds-home-details-chip'])[1]/header/h3/span[1]/span[1]/text()").get()
            baths = response.xpath("(//div[@class = 'ds-home-details-chip'])[1]/header/h3/span[3]/span[1]/text()").get()
            sqft = response.xpath("(//div[@class = 'ds-home-details-chip'])[1]/header/h3/span[5]/span[1]/text()").get()
            year =response.xpath("//ul[@class='ds-home-fact-list']/li[2]/span[2]/text()").get()
            lot_size = response.xpath("//ul[@class='ds-home-fact-list']/li[6]/span[2]/text()").get()
            street_address = response.xpath("(//div[@class = 'ds-home-details-chip'])[1]/div[1]/header/h1/span[1]/text()").get()
            city_address = response.xpath("(//div[@class = 'ds-home-details-chip'])[1]/div[1]/header/h1/span[2]/text()[2]").get()
            home_type = response.xpath("//ul[@class='ds-home-fact-list']/li[1]/span[2]/text()").get()
            zest = response.xpath("(//div[@class = 'ds-home-details-chip'])[1]/p/span[2]/span[2]/span[2]/text()").get()
            zrent = response.xpath("(//div[@class = 'ds-home-details-chip'])[1]/p/span[3]/span[3]/text()").get()
            zillow_url = response.url
 


            beds = clean_string_convert_to_float(beds)
            baths = clean_string_convert_to_float(baths)
            sqft = clean_string_convert_to_float(sqft)
            year = clean_string_convert_to_float(year)
            lot_size = clean_string_convert_lot(lot_size)
            street_address = clean_string(street_address)
            city_address = clean_string(city_address)
            zest = clean_string_convert_to_float(zest)
            zrent = clean_string_convert_to_float(zrent)
            home_type = clean_string(home_type)



            yield{
                'beds':beds,
                'baths':baths,
                'sqft':sqft,
                'year':year,
                'lot_size':lot_size,
                'street_address':street_address,
                'city_address':city_address,
                'home_type':home_type,
                'zest':zest,
                'zrent':zrent,
                'url':zillow_url}
        except:
            print('Failed to get data. Probably was a broken link')


