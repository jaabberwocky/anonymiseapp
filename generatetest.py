import pandas as pd
import random
import string
import names


def generatetest(n=100, filename="test_data"):
	ids = []
	names_list = []
	for _ in range(n):
		ids.append(''.join(random.choices(string.ascii_letters + string.digits, k=9)))
		names_list.append(names.get_full_name())

	df = pd.DataFrame({
		'id':ids,
		'names':names_list,
		})
	df.to_csv('data/{}.csv'.format(filename), index=False)
	
if __name__ == "__main__":
	generatetest()
	print("test set generated!")