import os

def create_environment():
	if os.path.isdir(os.path.join(os.getcwd(), "data")):
		pass
	else:
		os.mkdir("data")
	return None
