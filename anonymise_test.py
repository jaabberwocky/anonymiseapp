from application import anonymise

anonymise('test_data.csv', column="id", salt='test1234')
print("anonymise test done!")