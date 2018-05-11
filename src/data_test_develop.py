#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from lxml import etree
import pandas as pd
import requests
import config.constants as constant


def fast_iter(context, func):
    """
    Extended function originally produced by IBM, which parses very large xml files quickly and cleanly.
    :param context: The xml structure
    :param func: The function the method calls to process each instance of the Listing tag.
    :return: finalDF: The Dataframe containing all processed Listing tag rows.
    """
    # http://www.ibm.com/developerworks/xml/library/x-hiperfparse/
    finalListingDF = pd.DataFrame()
    for event, elem in context:
        # Each instance of Listing calls process_mls_xml for processing
        listingDF = func(elem)
        # Returns a single row datafrom which is appended to the final dataframe
        finalListingDF = finalListingDF.append(listingDF, ignore_index=True)
        # After usage, clear the current element and parent to free memory
        elem.clear()
        while elem.getprevious() is not None:
            del elem.getparent()[0]
    del context
    return finalListingDF

def assign_data_elements(context, newListingSet):
    """
    Assign the data elements from the provided xml structure to a Pandas DB
    :param context: Element tag containing data to be processed
    :param newListingSet: Dict containing items to be stored
    :return: df - single row Dataframe for the provided Element
    """
    listingDict = {}

    for containerKey in newListingSet:
        for key in newListingSet[containerKey]:
            try:
                # Check if the count of elements for the given xpath is greater than 1, if so
                # it is a list, and will need to be comma separated before being added to the Dict
                # Assumption made: Any time a list of elements are received they will be comma separated
                if len(context.xpath('{}/{}/text()'.format(containerKey, key))) > 1:
                    listingDict[containerKey.split("/")[-1]] = ','.join(context.xpath('{}/{}/text()'.format(containerKey, key)))
                else:
                # Otherwise add the value
                    listingDict[key] = context.xpath('{}/{}/text()'.format(containerKey, key))[0]
            except:
                # In the cases where a key does not have a value, set it to None
                listingDict[key] = None
    df = pd.DataFrame([listingDict], columns=listingDict.keys())
    return df

def filter_listing(elem):
    """
    Determine if the current element meets the filter inputs
    :param elem: Current element object of listing
    :return: Bool
    """
    is_valid = True
    for path, filterOption in constant.CONST_FILTER_LISTING_ELEMENTS.iteritems():
        # Only run the process for the year 2016 and for descriptions containing 'and'
        try:
            pathText = elem.xpath('{}/text()'.format(path))[0]
        except:
            return False

        if filterOption not in pathText:
            return False

    return True


def process_mls_xml(elem):
    """
    Process data for the mls feed xml.
    :param context: Element holding the defined iterparse
    :return: Dataframe containing the elements data, or null if the data does not meet the criteria
    """
    newListingDict = constant.CONST_PATH_DICT
    try:
        # Determine if the eleement meets the filter options
        if filter_listing(elem):
            df = assign_data_elements(elem, newListingDict)
            return df
    except:
        return

def get_xml_data(url):
    """
    Call the url using the Requests package to download the xml file
    :param url: The url to the host website
    :return: None
    """
    response = requests.get(url)

    if(response.status_code == 200):
        with open("in_file.xml", 'wb') as file_feed:
            file_feed.write(response.content)

    return response.status_code

def process_mls():
    """
    Initiates the process.
    :return: None
    """
    status_code = get_xml_data(constant.CONST_MLS_URL)

    if status_code == 200:
        context = etree.iterparse(constant.CONST_FEED_FILE, events=("end",), tag=constant.CONST_ITERABLE_FILTER_TAG)

        finalDF = fast_iter(context,process_mls_xml)

        # Final clean up, limit the description field to 200 characters, sort by the DateListed, order the columns and create the csv file
        finalDF[constant.CONST_MLS_COLUMNS[9]] = finalDF[constant.CONST_MLS_COLUMNS[9]].str[:199]
        finalDF = finalDF[constant.CONST_MLS_COLUMNS]
        finalDF.sort_values(by=[constant.CONST_MLS_COLUMNS[2]]).reset_index(drop=True).to_csv(constant.CONST_OUTPUT_CSV)
    else:
        print "Error::Failed to load xml data."

if __name__ == '__main__':
    process_mls()
