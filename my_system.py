import getpass
import subprocess
from classes.printer import bcolors, myprint
from classes.folder_manager import create_dir_if_not_already_there
from classes.ezpath import ezpath

class My_system():
	def __init__(self):
		self.username = getpass.getuser()
		self.dev_dir = "/Users/"+self.username+"/dev"
		self.quadf_dir = self.dev_dir + "/QuadF"
		self.apache_version = self.get_apache_version()
		self.java_version = self.get_java_version()
		
	def get_apache_version(self):
		apache = subprocess.Popen(["httpd", "-v"], stdout=subprocess.PIPE).communicate()[0]
		apache = apache.split("Server version: Apache/")[1].split(" (Unix)")[0].split(".")
		apache = apache[0]+"."+apache[1]
		return apache
		
	def get_java_version(self):
		java = subprocess.check_output(["java", "-version"], stderr=subprocess.STDOUT)
		java = java.split('java version "')[1].split('"')[0]
		return java
		
	# input: nothing
	# description: if dev isnt created, create it, if quadf isnt created, pull down from github
	# output: null	
	def clone_git(self):
		myprint("\nBegining to Clone QuadF from Github", bcolors.BOLD, True)	
	
		if create_dir_if_not_already_there(self.quadf_dir, "https://github.intuit.com/QuadF/QuadF.git"):
			myprint("Note: ", bcolors.BOLD, False)
			print "Delete Folders if you want them to be replaced."
			myprint("Successful Clone from Git\n", bcolors.OKGREEN, True)
		else:
			myprint("Note: ", bcolors.BOLD, False)
			print "Delete Folders if you want them to be replaced."
			myprint("Repository already cloned\n", bcolors.OKGREEN, True)	
			
	def restart_apache(self):
		myprint("Files Edited. Restarting Apache...", bcolors.BOLD, True)
		apache_check = subprocess.Popen(["httpd", "-t"], stdout=subprocess.PIPE).communicate()[0]
		if apache_check.find("Syntax OK"):																									
			subprocess.call(["sudo", "apachectl", "stop"])
			subprocess.call(["sudo", "apachectl", "start"])
			myprint("Apache restart complete\n", bcolors.OKGREEN, True)
		else:
			myprint("Syntax Error with Apache", bcolors.FAIL, True)
			
	def start_proxy(self):
		start_proxy_path= ezpath(self.quadf_dir+"/cfp-proxy/pom.xml")
		subprocess.call(["mvn", "tomcat:run", "-f", start_proxy_path])
		
	def update_json(self):
		myprint("Updating QuadF forms", bcolors.BOLD, True)
		# calls exactly what is writen in the string on the command line
		subprocess.call([self.quadf_dir+"/qa/scripts/webdevjsonupdate "+self.quadf_dir+"/client/web/qdf/"], shell = True) 
		myprint("Updating QuadF forms Complete\n", bcolors.OKGREEN, True)