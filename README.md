# Data Anonymiser!
[![Build Status](https://travis-ci.org/jaabberwocky/anonymiseapp.svg?branch=master)](https://travis-ci.org/jaabberwocky/anonymiseapp)

Simple data anonymiser app in **Flask** that implements the SHA256 hash function on a dataset on a column that the user specifies. Will also apply salt to the hash if given.

# How to run?
1. Run `python generatetest.py` to generate test_data.csv
2. Make sure dependencies are present. Run `pip install -r requirements.txt`, (*optional to use virtualenv*)
3. Run `python create_environment.py` to create environment
4. Run `python application.py` to run the app
5. Navigate to `http://localhost:5000` to see the app!

*Optional*
- Run `python testsetup.py` to remove the data folder's contents
(Note: should not be needed after commit `8d43be15f4881f4bcd05d0bd073bd184dcf4d263` as files are cleared after each session)
- Run `coverage tests.py` and `coverage report` to see tests and test coverage.

# Todo
~~1. Implement temp storage for files~~

2. Perform form validation, possibly with WTForms

~~3. Output pandas table to html to show users sample of data~~
