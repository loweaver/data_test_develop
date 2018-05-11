import os
import unittest
import requests
from lxml import etree

import src.data_test_develop as dtd
import config.constants as constant

class TestMlsMethods(unittest.TestCase):

    def setUp(self):
        self.test_valid = '{}/test/config/single_record_valid.xml'.format(os.getcwd())
        self.test_invalid = '{}/test/config/single_record_invalid.xml'.format(os.getcwd())

    def test_xml_data(self):
        response = requests.get(constant.CONST_MLS_URL)
        self.assertEqual(response.status_code, 200)

    def test_process_mls_xml_valid(self):
        context = etree.iterparse(self.test_valid, events=("end",), tag='Listing')

        for event, elem in context:
            df = dtd.process_mls_xml(elem)
        self.assertIsNotNone(df)

    def test_process_mls_xml_invalid(self):
        context = etree.iterparse(self.test_invalid, events=("end",), tag='Listing')

        for event, elem in context:
            df = dtd.process_mls_xml(elem)
        self.assertIsNone(df)

if __name__ == '__main__':
    unittest.main()
