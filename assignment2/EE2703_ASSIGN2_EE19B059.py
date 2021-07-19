	#EE2703 Assignment 2
#Name    : Vishnu Varma V
#Roll No : EE19B059

#importing all the modules required for this program
import numpy as np
import sys
import cmath
import math

#Instead of hard coding using .circuit , .end and .ac through out the program we use start , stop and AC these variables can be modified based on requirement
start = ".circuit"
stop = ".end"
AC = ".ac"
		
#Declarations
w = 0			#frequency of operation
ac_flag =0		#to  determine if the circuit is ac or not
node =[]		#list of node Objects
nodes =[] 		#list of node names
resistors = []		#list of all resistors
capacitors = []	#list of all capacitors
inductors = []		#list of all inductors
voltage_sources = []	#list of all voltage sources
current_sources = []	#list of all current sources

#This is the convention followed through out the program
#from = lower voltage
#to = higher voltage

#NODE class takes the node name and index as input, name, index, and other characteristics of that node can be accessed
class NODE: 
	def __init__(self,name,index): 
		self.name = name
		self.index = index
		self.from_imped = []
		self.to_imped = []
		self.from_V = []
		self.to_V = []
		self.from_I = []
		self.to_I = []

#IMPED class takes element name nodes across it and its value and type of element as input 		
class IMPED:
	def __init__(self,name,node1,node2,value,ele):
		#name of the element can be accessed
		self.name = name
		#node1 of the element can be accessed
		self.node1 = node1
		#node2 of the element can be accessed
		self.node2 = node2
		#if it is a resistor then its value will be the same
		if(ele == 'R'):
			self.value = value
		#if it is a capacitor and an ac circuit then its impedence is calculated
		elif(ele == 'C'):
			if(ac_flag):
				self.value = complex(0,-1/(w*value))
			#if it is capacitor and not an ac circuit then the capacitor will become open circuit so given such high value
			else:
				self.value = 1e100
		#if it is an inductor and an ac circuit then its impedence is calculated
		elif(ele == 'L'):
			if(ac_flag):
				self.value = complex(0,(w*value))
			#if it is inductor and not an ac circuit then the inductor will become short circuit so given such low value
			else:
				self.value = 1e-100
		self.ele = ele

#INDEPENDENT class takes name nodes across it and value and type of independent source as input		
class INDEPENDENT:
	def __init__(self,name,node1,node2,value,ele):
		#the inputs taken can be specifically accessed using this class
		self.name = name
		self.node1 = node1
		self.node2 = node2
		self.value = value
		self.ele = ele

#GND is the ground node and it is appended to the list of node names
nodes.append("GND")
#GND is made an object of NODE class
temp = NODE("GND",0)
#the object is appended into the list of node objects
node.append(temp)

#Reading the Circuit
def fileread():
    global ac_flag,w
    #for this program the number of arguments required is 2 so checking for that
    if(len(sys.argv)!=2):
        #if the number of arguments doesn't match then the user is given the output which displays the usage of commandline
        print("Usage %s <input file>" % argv[0])
        exit()
    #open() is executed and the result is stored in f, using with will take care of things like closing the file
	#argv[1] is the file passed as argument from commandline    
    with open(sys.argv[1]) as f:
        #f.readlines() returns a list of strings corresponding to each line in the file and it is stored in lines
        lines = f.readlines()
        #contains is used to store the tokens from each line
        contains = []
        #parsing through lines and splitting them
        for l in lines:
            tokens = l.split()
            #if it is an empty line then go to the next line
            if(len(tokens) == 0):
                continue
            #to  extract the lines starting from start    
            if (start== tokens[0]):
                flag = 1
                continue
            #ending parsing the lines when stop is encountered and start is already encountered    
            if flag:
                if ((stop == tokens[0]) and ((len(tokens)==1) or (tokens[1][0] =='#'))):
                    flag = 0
                    continue  
                #appending each line between start and stop into contains           
                contains.append(l)
            #if it is an ac circuit then frequency is being taken     
            if(AC == tokens[0]  and tokens[1][0] == 'V'):
                ac_flag = 1
                #alpha_to_value is a function defined below which converts any alphabets such as k - 1e3 and so on into numerical values
                w = alpha_to_value(tokens[2])
                print("Frequency :" , w)
                #f would be specified from the netlist so multiplying with 2pi gives w
                w = w* 2*math.pi
                break
        #if there are no lines between start and stop then the file is missing error is popped
        if(len(contains)==0):
            print("Empty File or missing %s flag" %(start))
            exit()
    #returning the contains when the function is called
    return contains
    
#alpha_to_value is a function defined below which converts any alphabets such as k is 1e3, m is 1e-3 and so on into numerical values
def alpha_to_value(x):
    y = len(x)
    #if there is no alphabet in the given value then it is converted to float and passed as it is
    if(not x[y-1].isalpha()):
        return float(x)
    #general convention of naming alphabets and their corresponding values are assigned
    if(x[y-1]=='p'):
        return float(x[0:y-1])* 1e-12   
    if(x[y-1]=='n'):
        return float(x[0:y-1])* 1e-9
    if(x[y-1]=='u'):
        return float(x[0:y-1])* 1e-6
    if(x[y-1]=='m'):
        return float(x[0:y-1])* 1e-3
    if(x[y-1]=='k'):
        return float(x[0:y-1])* 1e3
    if(x[y-1]=='M'):
        return float(x[0:y-1])* 1e6
    if(x[y-1]=='G'):
        return float(x[0:y-1])* 1e9  

#when an element is specified then the corresponding two nodes are passed to this function        
def append(n1,n2):
    #if either of the nodes is not alphanumeric then error is shown
    if(not (n1.isalnum() and n2.isalnum())):
        print("Node names must be alphanumeric Please Check circuit definition")
        exit()
    if(n1 not in nodes):
        #each node is appended in the list of nodes 
        nodes.append(n1)
        #node name and its index in the nodes list is made an object in NODE class
        temp = NODE(n1,nodes.index(n1))
        #the object created in NODE class is appended into the list of node objects list
        node.append(temp)
    #Similarly the other node is appended into nodes and corresponding object is appended into node[]
    if(n2 not in nodes):
        nodes.append(n2)
        temp = NODE(n2,nodes.index(n2))
        node.append(temp)
    #corresponding node indexes from nodes list is returned     
    return nodes.index(n1),nodes.index(n2)

#this function parses through each line recognizes the components and append the same in respective lists
def parse_line(line):
    #if any comments are present in the line then it is neglected and remaining part is parsed
    tokens = line.split('#')[0].split()
    l = len(tokens)
    #based on the length of tokens the components are classified 
    #when l == 4 then it should be a resistor or capacitor or inductor or voltage source or current source 
    if(l==4 and(tokens[0][0] == 'R' or tokens[0][0] == 'L' or tokens[0][0] == 'C' or tokens[0][0] == 'V' or tokens[0][0] == 'I')):
        #corresponding name, nodes, value are stored in ele n1, n2 and value
        ele = tokens[0]
        n1 = tokens[1]
        n2 = tokens[2]
        value = tokens[3]
        #value can be specified in alphanumeric so passing the value through alpha_to_value to get the correct value
        val = alpha_to_value(value)
        #passing the nodes across the elements to append function
        #append function appends these nodes into list of nodes and corresponding node objects in node list
        from_node_index,to_node_index = append(n1,n2) 
        #R C L are all considered as impedences so the value obtained are made as objects in IMPED class 
        if(tokens[0][0] == 'R' or tokens[0][0] == 'C' or tokens[0][0] == 'L'):
            x = IMPED(ele,from_node_index,to_node_index,val,tokens[0][0])
            #the objects from IMPED class is appended to the object present in node list the values are specified under .from_imped and .to_imped
            node[from_node_index].from_imped.append(x)
            node[to_node_index].to_imped.append(x)
            #the values are appended into corresponding elements list
            if(tokens[0][0] == 'R'):
                resistors.append(x)            
            if(tokens[0][0] == 'L'):
                inductors.append(x)
            if(tokens[0][0] == 'C'):
                capacitors.append(x) 
        #if there is no element as such then there doesn't exist such circuit so there is some syntax error
        else:
            print("Syntax Error in netlist File")
    #if l == 6 then it is an ac votage or current source         
    elif(l == 6):
        if((tokens[0][0] == 'V' or tokens[0][0] == 'I') and (tokens[3] == 'ac')):
            #corresponding name, nodes, value are stored in ele n1, n2 and value
            ele = tokens[0]
            n1 = tokens[1]
            n2 = tokens[2]
            #value can be specified in alphanumeric so passing the value through alpha_to_value to get the correct value
            value = alpha_to_value(tokens[4])
            #since the specified value is peak to peak it is divided by 2 to get value used in our calculations
            value = value/2
            phase = alpha_to_value(tokens[5])
            #append function appends these nodes into list of nodes and corresponding node objects in node list
            from_node_index,to_node_index = append(n1,n2)
            #x is an object in INDEPENDENT class all the required arguments are passed 
            #value would be in polar form so converting polar into rectangular and passing
            x = INDEPENDENT(ele,from_node_index,to_node_index,complex(value*math.cos(phase),math.sin(phase)),tokens[0][0])
            #for voltage source voltage value is stored in voltage_sources and the objects of INDEPENDENT class are appended into from and to properties of node list
            if(tokens[0][0] == 'V'):
                voltage_sources.append(x)
                node[from_node_index].from_V.append(x)
                node[to_node_index].to_V.append(x)
            #for current source current value is stored in current_sources and the objects of INDEPENDENT class are appended into from and to properties of node list    
            if(tokens[0][0] == 'I'):
                current_sources.append(x)
                node[from_node_index].from_I.append(x)  
                node[to_node_index].to_I.append(x)
        #if it is neither voltage nor current source then the properties of elements is stored and checked if all are alphanumeric and corresponding error is shown if it is not satisfied        
        else:
            ele = tokens[0]
            n1 = tokens[1]
            n2 = tokens[2]
            n3 = tokens[3]
            n4 = tokens[4]
            value = tokens[5]
            if(not (n1.isalnum() and n2.isalnum() and n3.isalnum() and n4.isalnum())):
                print("Nodes must be alphanumeric")
                exit()
    #if l == 5 then it is a dc votage or current source            
    elif(l == 5):
        if((tokens[0][0] == 'V' or tokens[0][0] == 'I') and tokens[3] == 'dc'):
            #since it is dc and if ac_flag is 1 then error because there are multiple frequencies
            if(ac_flag):
                print("Error : Multiple frequencies in same circuit")
                exit()
            #corresponding name, nodes, value are stored in ele n1, n2 and value
            ele = tokens[0]
            n1 = tokens[1]
            n2 = tokens[2]
            #value can be specified in alphanumeric so passing the value through alpha_to_value to get the correct value
            value = alpha_to_value(tokens[4])
            #append function appends these nodes into list of nodes and corresponding node objects in node list
            from_node_index,to_node_index = append(n1,n2)
            #for voltage source voltage value is stored in voltage_sources and the objects of INDEPENDENT class are appended into from and to properties of node list
            if(tokens[0][0] == 'V'):
                x = INDEPENDENT(ele,from_node_index,to_node_index,value,tokens[0][0])
                voltage_sources.append(x)  
                node[from_node_index].from_V.append(x)  
                node[to_node_index].to_V.append(x)        
            #for current source current value is stored in current_sources and the objects of INDEPENDENT class are appended into from and to properties of node list
            if(tokens[0][0] == 'I'):
                x = INDEPENDENT(ele,from_node_index,to_node_index,value,tokens[0][0])
                current_sources.append(x)
                node[from_node_index].from_I.append(x)  
                node[to_node_index].to_I.append(x)  
        #if it is neither voltage nor current source then the properties of elements is stored and checked if all are alphanumeric and corresponding error is shown if it is not satisfied    
        else:   
            ele = tokens[0]
            n1 = tokens[1]
            n2 = tokens[2]
            V = tokens[3]
            value = tokens[4]
            if(not (n1.isalnum() and n2.isalnum())):
                print("Node names are alphanumeric")

    return
    
#this function constructs M matrix which is the MNA matrix
def construct_M():
    #if ac flag is 1 then the entries in the matrix are complex else they are real values
    #unknowns are node voltages and current through voltage sources which are the corresponding rows and columns of MNA matrix
    if(ac_flag==1):
        M = np.zeros((len(node)+len(voltage_sources),len(node)+len(voltage_sources)),dtype=complex)
        b = np.zeros(len(node)+ len(voltage_sources),dtype=complex)
    else:
        M = np.zeros((len(node)+len(voltage_sources),len(node)+len(voltage_sources)))
        b = np.zeros(len(node)+ len(voltage_sources))
    #adding all the terms to the matrix related to impedences    
    for n in node:
        #the ground voltage is assigned to 0V first row in the matrix corresponds to this equation 
        if(n.name == "GND"):
            M[0][0] = 1
            b[0] = 0
            continue
        #when MNA analysis is made 1/impedence_value and -1/impedence_value are added at corresponding nodal positions of the matrix    
        for x in n.to_imped:
            M[node.index(n)][x.node1] += (1/x.value)
            M[node.index(n)][node.index(n)] -= (1/x.value)    
        for x in n.from_imped:
            M[node.index(n)][x.node2] += (1/x.value)
            M[node.index(n)][node.index(n)] -= (1/x.value)

    #voltage equations when written subtraction of node voltages and equating the difference to voltage value provides the values in matrix for voltage sources
    #in this analysis from is taken as negative and to is taken as positive
    #IMPORTANT : from = -ve and to = +ve
    for x in voltage_sources:
        M[x.node1][voltage_sources.index(x)+len(node)] -=1
        M[x.node2][voltage_sources.index(x)+len(node)] +=1
        M[voltage_sources.index(x)+len(node)][x.node1] -=1    
        M[voltage_sources.index(x)+len(node)][x.node2] +=1    
        b[voltage_sources.index(x)+len(node)] = x.value
    #from is current leaving and to is current entering   
    #for ac /2 beacuse it is peak to peak for dc it is just the value         
    for x in current_sources:
        if(ac_flag==1):
            b[x.node1] += x.value/2                  #from = leaving
            b[x.node2] -= x.value/2                   #to = entering
        else:
            b[x.node1] += x.value                   
            b[x.node2] -= x.value
    M[0][len(node):] = np.zeros(len(voltage_sources))
    b[0] = 0
    return M,b

#Reading the netlist file removing comments and printing along with passing the lines to parse_line to determine values required to construct MNA matrix
for l in fileread():
    #removing comments
    a = l.split('#')[0].split()
    #output the netlist between start and stop removing comments
    print(' '.join(a))
    parse_line(l)
#construct_M constructs MNA matrix corresponding M and b are assigned 
M,b = construct_M()
#output M and b
print("\nM : \n",M)
print("\nb : \n",b)
#solving for nodal voltages and currents through voltage sources using np.linalg.solve function
try:
    X = np.linalg.solve(M,b)
    print("\n X: \n",X)
#if it could not be solved then output error
except:
    print("Unsolvable Matrix")
    exit()
#output nodal voltages and current through voltage sources rounding off the magnitude and phase to 4 decimals    
print("\n")
i=0
for n in nodes:
    print("Voltage at Node " + n+" : mag = ", round(abs(X[i]),4), end = '')
    print("  phase(deg) =",round(np.degrees(cmath.phase(X[i])),4)) 
    i = i+1
for V in voltage_sources:
    print("Current Through Voltage Source " + V.name + " : mag = ", round(abs(X[i]),4), end = '')
    print("  phase(deg) =",round(np.degrees(cmath.phase(X[i])),4))
    i= i+1                     

