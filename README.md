# Data Anonymiser!

Simple data anonymiser app in **Flask** that implements the SHA256 hash function on a dataset on a column that the user specifies. Will also apply salt to the hash if given.

# How to run?
1. Run `python generatetest.py` to generate test_data.csv
2. Run `python create_environment.py` to create environment
2. Run `python application.py` to run the app
3. Navigate to `http://localhost:5000` to see the app!

*Optional*
1. Run `python testsetup.py` to remove the data folder's contents
(Note: should not be needed after commit `8d43be15f4881f4bcd05d0bd073bd184dcf4d263` as files are cleared after each session)

# Todo
~~1. Implement temp storage for files~~
2. Perform form validation, possibly with WTForms
~~3. Output pandas table to html to show users sample of data~~
