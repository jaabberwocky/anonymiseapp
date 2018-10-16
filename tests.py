import unittest
import shutil
import hashlib
import os
import sys
from create_environment import create_environment
from generatetest import generatetest

# load in application
from app import hashthis, anonymise, application, returnhtmlview

class ApplicationTests(unittest.TestCase):

    def setUp(self):
        ''' make sure that the test_data set is created each time
        '''
        create_environment()
        generatetest()
        application.config['Testing'] = True
        
    def tearDown(self):
        shutil.rmtree("data")

    def test_hashthis(self):
        '''
        tests the hash_this function
        '''
        s = "hello world"
        salt = "salt"
        hash_string = salt + s
        hashed = hashlib.sha256(hash_string.encode()).hexdigest()
        self.assertEqual(hashed, hashthis("hello world", "salt"))
    
    def test_anonymise_exists(self):
        '''
        checks if the anonymise function has created a processed file
        '''
        completed_filename = anonymise('test_data.csv', column='id')
        self.assertTrue(os.path.isfile(os.path.join(os.getcwd(),"data",str(completed_filename) + ".csv")))

    def test_htmlview(self):
        '''
        checks if returnhtmlview returns something
        '''
        html = returnhtmlview('test_data.csv')
        self.assertIsNotNone(html)

if __name__ == "__main__":
    unittest.main()
