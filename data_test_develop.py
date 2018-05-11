#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from lxml import etree

def fast_iter(context, func):
    """
    Extended function originally produced by IBM, which parses very large xml files in a memory conscious way.
    :param context: The xml structure
    :param func: The function the method calls to process each instance of the Listing tag.
    :return: finalDF: The Dataframe containing all processed Listing tag rows.
    """
    # http://www.ibm.com/developerworks/xml/library/x-hiperfparse/
    for event, elem in context:
        func(elem)
        print(elem)
        elem.clear()
        while elem.getprevious() is not None:
            del elem.getparent()[0]
    del context

def process_mls_xml(context):
    pass

def process_mls():
    context = etree.iterparse("listings.xml", events=("end",), tag='Listing')
    fast_iter(context,process_mls_xml)

if __name__ == '__main__':
    process_mls()