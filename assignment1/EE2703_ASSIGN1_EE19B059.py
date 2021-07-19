	#EE2703 Assignment 1
#Name    : Vishnu Varma V
#Roll No : EE19B059

#We need arguments to the program from the commandline, sys module is used to access the commandline arguments
from sys import argv, exit
#for this program the number of arguments required is 2 so checking for that
if len(argv) != 2:
	#if the number of arguments doesn't match then the user is given the output which displays the usage of commandline	
	print("Usage %s <input file>" % argv[0])
	exit()
#Instead of hard coding using .circuit and .end through out the program we use start and stop these variables can be modified based on requirement
start = '.circuit'
stop = '.end'
#If a wrong file name is entered then an IOError will pop up so to avoid that we have used try and exception handling below
try:
	#open() is executed and the result is stored in f, using with will take care of things like closing the file
	#argv[1] is the file passed as argument from commandline 
	with open(argv[1]) as f:
		#f.readlines() returns a list of strings corresponding to each line in the file and it is stored in content
		content = f.readlines()
		#start_index and stop_index are the index values where start and stop are found the reqired information of the file is found between these two indices, if there is no start and stop then an error will pop up
		#m and n are variables to account for the number of times .circuit and .end occur in the file
		start_index = -1 ; stop_index = -2; m=0; n=0
		#Iterating through each line of the content to check for start and stop and storing the respective index vaue in start_index and stop_index
		for l in content:
			#checking only the first required number of elements of each line with the required element, required number is obtained using len(start) and len(stop)
			if start == l[:len(start)]:
				#m is the number of times .circuit occurs in the file
				m += 1
				#if the condition is satisfied then start_index is initialised with the value of index of that line
				start_index = content.index(l)
			#Similarly stop_index is initialised
			elif stop == l[:len(stop)]:
				#n is the number of times .end occurs in the file
				n += 1
				stop_index = content.index(l) 
				
		#If there are multiple .circuit or .end in a file then a error message will pop up		
		if m>1 or n>1:
			print("Multiple %s or %s Please check circuit definition" % (start,stop))
			exit(0)
			
		#Now we have start_index and stop_index comparing them to give an error message if start_index is greater than or equal to stop_index
		if start_index >= stop_index:
			print("Circuit Invalid : Please check the circuit definition")
			exit(0)
			
		#x is an array used to store the strings from content in reverse order
		x = []
		#Iterating through each line in content REVESING that particular line and storing in x
		for l in content[start_index+1:stop_index]:
		#' '.join() combines the elements of an array of strings into a string seperated by spaces and split('#')[0] removes comments if any in content
			x.append(' '.join(reversed(l.split('#')[0].split())))
			
		#a is another array which stores the lines of array x in reverse order
		a = x[-1::-1]
		#Displaying output a
		for i in range(0,len(a)):
			#If a line in the file starts with # which is a comment it is already removed but an empty line will be printed to avoid that this condition is used
			if a[i] != "":
				print(''.join(a[i]))
				
#if the file name is wrong then it is taken care using exception handling to prevent IOError
except IOError:
    print('File not found')
    exit()
