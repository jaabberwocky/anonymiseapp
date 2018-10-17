import unittest
from flask_testing import TestCase
import shutil
import hashlib
import os
import sys
from bs4 import BeautifulSoup as bs
from flask import url_for
from create_environment import create_environment
from generatetest import generatetest

# load in application
from app.app import hashthis, anonymise, application, returnhtmlview, returncolnames


class ApplicationTests(TestCase):

    def setUp(self):
        ''' 
        make sure that the test_data set is created each time
        '''
        create_environment()
        generatetest()
        application.config['Testing'] = True
        # we can then access the below as self.client
        self.client = application.test_client()

    def tearDown(self):
        shutil.rmtree("data")

    def create_app(self):

        app = application
        app.config['TESTING'] = True
        return app

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
        self.assertTrue(os.path.isfile(os.path.join(
            os.getcwd(), "data", str(completed_filename) + ".csv")))

    def test_htmlview(self):
        '''
        checks if returnhtmlview returns valid html
        '''
        html = returnhtmlview('test_data.csv')
        self.assertTrue(bool(bs(html, "html.parser").find()))

    def test_returncolnames(self):
        '''
        checks if returncolnames returns the correct colnames for test_data (id, names)
        '''
        colnames = returncolnames('test_data.csv')
        self.assertEqual(colnames, ['id', 'names'])

    def test_index(self):
        '''
        check if index is 200
        '''

        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

    def test_upload_render(self):
        '''
        check if upload is 200
        '''
        client = self.client
        resp = client.get('/upload')
        self.assertEqual(resp.status_code, 200)

    def test_upload_redirect(self):
        '''
        check if upload is working correctly with redirect
        '''
        client = application.test_client(use_cookies=True)
        data = dict()
        # we use this to OPEN our test data created in setUp
        # make sure follow_redirects is not specified, otherwise you will get 200 response
        # from '/selectcolumn'
        with open(os.path.join(os.getcwd(), "data", "test_data.csv"), 'rb') as f:
            data['datafile'] = (f, f.name)
            resp = client.post(
                '/upload',
                data=data,
                headers={'content-Type': 'multipart/form-data'})
        self.assertRedirects(resp, "/selectcolumn")

    def test_selectcolumn(self):
        '''
        check if selectcolumn post method is working correctly
        '''
        with self.client as c:
            with c.session_transaction() as sess:
                sess['filename'] = "test_data.csv"
            resp = c.post('/selectcolumn', data={"salt":"", "column":"id"})
            self.assertRedirects(resp, "/processfile?column=id&salt=")

if __name__ == "__main__":
    unittest.main()
