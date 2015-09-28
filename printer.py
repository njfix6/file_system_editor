from platform import system

# colors for printing in command line
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
		
		
					
# input: 1: the word that needs to be printed. 2: the color that you want to be printed, or bold, etc. 3. Whether or not you want a new line
# description: prints out something with the specific style
# output: just print, return null
def myprint(word, color, new_line=False):
    if system() == "Darwin":
    	print (color + word + bcolors.ENDC),
    	if new_line:
    		print("")
    else:
        print (word),
        if new_line:
            print("")