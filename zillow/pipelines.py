import sqlite3




class EvasnsvilleSoldPipeline(object):

    #open the connection and create table if necesarry
    def open_spider(self, spider):
        #create or connect to the database
        self.connection = sqlite3.connect(r'C:\Users\josia\projects\zillow\databases\property_sale_prices_pt.db')
        #create a cursor
        self.c = self.connection.cursor()
        #create the table
        try:
            self.c.execute('''
                CREATE TABLE centralia_sold(
                    db_key TEXT,
                    address TEXT NOT NULL,
                    sale_price REAL,
                    sale_date,
                    beds REAL,
                    baths REAL,
                    sqft REAL,
                    year_built REAL,
                    home_type TEXT,
                    lot_size REAL,
                    parking TEXT,
                    heating TEXT,
                    cooling TEXT,
                    elementary_school_rating REAL,
                    middle_school_rating REAL,
                    high_school_rating REAL,
                    elementary_school TEXT,
                    middle_school TEXT,
                    high_school TEXT,
                    zest REAL,
                    z_rent_estimate REAL,
                    home_description TEXT,
                    latitude REAL,
                    longitude REAL,
                    confidence REAL,
                    looked_up_address TEXT,
                    link TEXT,
                    UNIQUE(db_key)
                )
            
            ''')

            print('succesfully created table')
            #commit the changes
            self.connection.commit()
        #this is a way to handle if the table already exists... there may be better methods to do this, but this works
        except sqlite3.OperationalError:
            pass


    #close the connection
    def close_spider(self, spider):
        self.connection.close()

    
    
    
    def process_item(self, item, spider):
        self.c.execute('''
            INSERT INTO centralia_sold(db_key,address,sale_price,sale_date,beds,baths,sqft,year_built,home_type,lot_size,parking,heating,cooling,elementary_school_rating,middle_school_rating,
            high_school_rating,elementary_school,middle_school,high_school,zest,z_rent_estimate,home_description,latitude,longitude,confidence,looked_up_address,link) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        
        ''',(
            item.get('db_key'),
            item.get('address'),
            item.get('sale_price'),
            item.get('sale_date'),
            item.get('beds'),
            item.get('baths'),
            item.get('sqft'),
            item.get('year_built'),
            item.get('home_type'),
            item.get('lot_size'),
            item.get('parking'),
            item.get('heating'),
            item.get('cooling'),
            item.get('elementary_school_rating'),
            item.get('middle_school_rating'),
            item.get('high_school_rating'),
            item.get('elementary_school'),
            item.get('middle_school'),
            item.get('high_school'),
            item.get('zest'),
            item.get('z_rent_estimate'),
            item.get('home_description'),
            item.get('latitude'),
            item.get('longitude'),
            item.get('confidence'),
            item.get('looked_up_address'),
            item.get('link')

        ))
        #commit the changes
        self.connection.commit()

        return item










#general property information from Zillow
class CentpropPipeline(object):

    #open the connection and create table if necesarry
    def open_spider(self, spider):
        #create or connect to the database
        self.connection = sqlite3.connect(r'C:\Users\josia\projects\zillow\databases\general_property_information.db')
        #create a cursor
        self.c = self.connection.cursor()
        #create the table
        try:
            self.c.execute('''
                CREATE TABLE centralia(
                    street_address TEXT NOT NULL,
                    city_address TEXT,
                    beds REAL,
                    baths REAL,
                    sqft REAL,
                    year REAL,
                    home_type TEXT,
                    lot_size REAL,
                    zest REAL,
                    zrent,
                    zillow_url TEXT,
                    UNIQUE(street_address)
                )
            
            ''')

            print('succesfully created table')
            #commit the changes
            self.connection.commit()
        #this is a way to handle if the table already exists... there may be better methods to do this, but this works
        except sqlite3.OperationalError:
            pass


    #close the connection
    def close_spider(self, spider):
        self.connection.close()

    
    
    
    def process_item(self, item, spider):
        self.c.execute('''
            INSERT INTO centralia(street_address,city_address,beds,baths,sqft,year,home_type,lot_size,zest,zrent,zillow_url) VALUES(?,?,?,?,?,?,?,?,?,?,?)
        
        ''',(
   
            item.get('street_address'),
            item.get('city_address'),
            item.get('beds'),
            item.get('baths'),
            item.get('sqft'),
            item.get('year'),
            item.get('home_type'),
            item.get('lot_size'),
            item.get('zest'),
            item.get('zrent'),
            item.get('url')

        ))
        #commit the changes
        self.connection.commit()

        return item















# #example to learn on
# class SQLlitePipeline(object):

#     #open the connection and create table if necesarry
#     def open_spider(self, spider):
#         #create or connect to the database
#         self.connection = sqlite3.connect(r'C:\Users\josiahh\projects\zillow\databases\learning.db')
#         #create a cursor
#         self.c = self.connection.cursor()
#         #create the table
#         try:
#             self.c.execute('''
#                 CREATE TABLE testing_setup(
#                     address TEXT NOT NULL,
#                     asking_price REAL,
#                     beds REAL,
#                     baths REAL,
#                     sqft REAL,
#                     whos_selling TEXT,
#                     realtor TEXT,
#                     day_on_zillow TEXT,
#                     link TEXT,
#                     UNIQUE(address)
#                 )
            
#             ''')
#             #commit the changes
#             self.connection.commit()
#         #this is a way to handle if the table already exists... there may be better methods to do this, but this works
#         except sqlite3.OperationalError:
#             pass


#     #close the connection
#     def close_spider(self, spider):
#         self.connection.close()

    
    
    
#     def process_item(self, item, spider):
#         self.c.execute('''
#             INSERT INTO testing_setup(address,asking_price,beds,baths,sqft,whos_selling,realtor,day_on_zillow,link) VALUES(?,?,?,?,?,?,?,?,?)
        
#         ''',(
#             item.get('address'),
#             item.get('asking_price'),
#             item.get('beds'),
#             item.get('baths'),
#             item.get('sqft'),
#             item.get('whos_selling'),
#             item.get('realtor'),
#             item.get('day_on_zillow'),
#             item.get('link')

#         ))
#         #commit the changes
#         self.connection.commit()

#         return item














