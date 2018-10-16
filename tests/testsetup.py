import os
import glob
import json

f = json.loads(open("config.json", "r").read())

# deletes all files previously uploaded so we can start with clean slate
def deletefiles():
	files = glob.glob(f["SAVE_FILE_DESTINATION"]+'/*')
	num_files = len(files)
	for file in files:
		os.remove(file)
	print("%d files deleted!" % num_files)
	return None

if __name__ == "__main__":
	deletefiles()