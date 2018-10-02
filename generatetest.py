import pandas as pd
import random
import string
import names


def main():
	ids = []
	names_list = []
	for _ in range(100):
		ids.append(''.join(random.choices(string.ascii_letters + string.digits, k=9)))
		names_list.append(names.get_full_name())

	df = pd.DataFrame({
		'id':ids,
		'names':names_list,
		})
	df.to_csv('test_data.csv', index=False)

if __name__ == "__main__":
	main()