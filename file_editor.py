import os
import sys
from platform import system

from printer import myprint, bcolors

from isarg import isarg
import subprocess
from ezpath import ezpath

# input: a path to a folder
# description: makes it so you can use \ and ~ for paths
# output: returns the folder object with the path
def ezpath(pathname):
	return os.path.expanduser(pathname)


###########################################
# START of File Editor classe
###########################################
class File_editor():
	def __init__(self, path, args):
		self.path = self.ezpath(path)
		self.args = args
		self.edited = False
		
	
	def create_file(self, string = ""):
		path = ezpath(self.path)
		if not os.path.isfile(path):
			 f = open(self.path, "w")
			 if string:
				 f.write(string)
			 f.close()
	
	def readlines(self):
		
		f = open(self.path, "r")
		return f.read()
	
	# input: input a string and a ezpath to a file
	# description: opens the file and returns whether the string exists in the file
	# output: returns true if the string exists, otherwise false		
	def __line_in_file(self, string):
		myfile = self.open_file(self.path, "r+")
		lines = myfile.readlines()
		found = False
		for line in lines:
			if string in line:
				return True
		myfile.close()
		return False
		
		
	# input: 1. the string that you want to see if it exists or not. 2. the string that you want to put in the file
	# description: if the find_string exists, do nothing, else append the replace_string to the file
	# output: true if edited, false if not	
	def append_file_with_string(self, find_string, replace_string):
		if isarg(self.args, '-f') and system() == "Darwin":
			subprocess.call(["sudo","chmod", "666", self.path])
		try:
			if self.__line_in_file(find_string):
				myprint("String:", bcolors.BOLD, False)
				print ("'"+replace_string[0:10]+"...'"),
				myprint("was already added to: ", bcolors.BOLD, False)
				print self.path+"\n"
				self.edited = False
	
			else:
				myfile = self.open_file(self.path, "a")
				myfile.write("\n"+"#The lines below were added by the environment setup script:\n"+replace_string)
				myfile.close()
				
				myprint("String:", bcolors.BOLD, False)
				print ("'"+replace_string[:10]+"...'"),
				myprint("added to: ", bcolors.BOLD, False)
				print self.path+"\n"
				self.edited = True
		except IOError:
			return
		
				
		
			
	# input: a path to a folder
	# description: makes it so you can use \ and ~ for paths
	# output: returns the folder object with the path
	def ezpath(self,pathname):
		return os.path.expanduser(pathname)
		
	def open_file(self, pathname, arg):		
		try:
			myfilepath = ezpath(pathname)	
			myfile = open(myfilepath, arg)
			return myfile
		except IOError:
			myprint("File does not exist: "+pathname+"\n", bcolors.FAIL, True)			
			self.edited = False
			raise IOError

	def template(self, line, template):
		for key, value in template.iteritems():
			line = line.replace(key, value)
		return line
			
			
	# input: 1. the string that you want to see if it exists or not. 
	#  		 2. the file with the text that you want to be put into the file 
	#	 	 3. argument for opening the file, ex: a for append, w for write 
	#        4. whether or not you want the templateing feature
	# description: if the find_string exists, do nothing, else, depending on the args, write, append, etc. the file with the replace_file_path. 
	#              template is true if you want to replace words. {{username}} is being replaced write now but more can be added.
	# output: if edited, self.edited = true, else false	
	def edit_file_with_file(self, find_string, replace_file_path, args, template = {}):
		if isarg(self.args, '-f') and system() == "Darwin":
			subprocess.call(["sudo","chmod", "666", self.path])
		try:
			if self.__line_in_file(find_string):
				myprint("The text from File:", bcolors.BOLD, False)
				print (replace_file_path),
				myprint("was already added to: ", bcolors.BOLD, False)
				print self.path+"\n"
				self.edited = False
	
			else:		
				with self.open_file(replace_file_path, "r") as read_file:
					with self.open_file(self.path, args) as append_file:
						append_file.write("\n"+"#The lines below were added by the environment setup script:\n")
						for line in read_file:
							if template:
								line = self.template(line, template)
							append_file.write(line)
						append_file.close()
						read_file.close()
	
				
				myprint("The text from File:", bcolors.BOLD, False)
				print (replace_file_path),
				myprint("added to: ", bcolors.BOLD, False)
				print self.path+"\n"
				self.edited = True
		except IOError:
			myprint("Failed to edit file", bcolors.FAIL, True)
			myprint("Program Stopped \n", bcolors.FAIL, True)
			sys.exit()
		
	
			
	
		
		
	# uncomments the line that matches the string_of_line
	def uncomment(self, string_of_line):
		if isarg(self.args, '-f') and system() == "Darwin":
			subprocess.call(["sudo","chmod", "666", self.path])
		try:
			myfile = self.open_file(self.path, "r")
			data = myfile.readlines()
			for n,i in  enumerate(data):
				if string_of_line in i:
					if '#' in i:
						self.edited = True
						data[n] = i.replace("#","")
						myprint("Uncommenting:", bcolors.BOLD, False)
						print ("'"+string_of_line[0:10]+"...'\n")
					else:
						myprint("String:", bcolors.BOLD, False)
						print ("'"+string_of_line[0:10]+"...'"),
						myprint("already uncommented\n", bcolors.BOLD, True)
						self.edited = False
			myfile.close()
			with open(self.path, "w") as f:
				f.writelines(data)
				f.close()
		except IOError:
			myprint("Failed to uncomment lines", bcolors.FAIL, True)
			myprint("Program Stopped \n", bcolors.FAIL, True)
			sys.exit()
		
			
			
			
###########################################
# END File Editor class
###########################################
