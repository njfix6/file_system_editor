import os

from ezpath import ezpath
import subprocess

# input: a pathname and a github directory if you want to get something from github
# description: if file already there, do nothing, else create the folder
# output: returns true if edited, else false
def create_dir_if_not_already_there(pathname, dir_from_github = ""):
	folder = ezpath(pathname)
	if not os.path.exists(folder):
		if dir_from_github:
			subprocess.call(["git", "clone", dir_from_github, folder])
			
		else:
			print "Creating: "+ folder
			os.makedirs(folder)
		return True
	else:
		print ("Folder already created: "+folder)
		False
		
		
		
# input: a ezpath created by the function above
# description: if the folder is already there, it deletes and creates it, otherwise it just creates it
# output: just creates a folder. return null.
# !!!!! uncomment below if you want to use this
# def delete_and_create_dir(pathname):
# 	if os.path.exists(pathname):
# 		shutil.rmtree(pathname)
# 	print "Updating: "+pathname
# 	os.makedirs(pathname)