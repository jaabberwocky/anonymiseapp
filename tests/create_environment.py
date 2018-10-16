import os

if os.path.isdir(os.path.join(os.getcwd(), "data")):
	pass
else:
	os.mkdir("data")

print("Completed!")