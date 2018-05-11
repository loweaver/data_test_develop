# Mapping of required items to be processed
CONST_PATH_DICT = {
    'ListingDetails': ('MlsId', 'MlsName', 'DateListed', 'Price',),
    'Location': ('StreetAddress',),
    'BasicDetails': ('Bedrooms','Bathrooms','Description',),
    'RichDetails/Appliances': ('Appliance',),
    'RichDetails/Rooms': ('Room',),
}

# URL to get the xml object
CONST_MLS_URL = 'http://syndication.enterprise.websiteidx.com/feeds/BoojCodeTest.xml'

# Order of columns
CONST_MLS_COLUMNS = ['MlsId','MlsName','DateListed','StreetAddress','Price','Bedrooms','Bathrooms','Appliances','Rooms','Description']

CONST_ITERABLE_FILTER_TAG = 'Listing'
CONST_DATE_FILTER_PATH = 'ListingDetails/DateListed'
CONST_DESC_FILTER_PATH = 'BasicDetails/Description'

CONST_FILTER_LISTING_ELEMENTS = {
    CONST_DATE_FILTER_PATH: '2016-',
    CONST_DESC_FILTER_PATH: ' and '
}

CONST_OUTPUT_CSV = "Mls_feed.csv"
CONST_FEED_FILE = "in_file.xml"
