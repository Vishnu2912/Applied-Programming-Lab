	#EE2703 Assignment 6
#Name    : Vishnu Varma V
#Roll No : EE19B059

#importing all the modules required
import numpy as np
import matplotlib.pyplot as plt
from sys import argv, exit
from tabulate import tabulate

#if there are no inputs for parameters from commandline then setting them to the default values
if(len(argv) == 1):
    print("Using the default parameters\n n = 100\n M = 5\n nk = 500\n u0 = 5\n p = 0.25\n Msig = 2\n")
    #spatial grid size
    n = 100
    #number of electrons injected per turn
    M = 5 
    #number of turns to simulate
    nk = 500
    #threshold velocity
    u0 = 5
    #probability that ionization will occur
    p = 0.25
    #Standard Deviation
    Msig = 2
#if the parameter values are specified then allocating them respectively
elif(len(argv) == 7):
    n = int(argv[1])
    M = int(argv[2])
    nk = int(argv[3])
    u0 = float(argv[4])
    p = float(argv[5])
    Msig = float(argv[6])
#if neither of the case is satisfied then prompting the method to run the code
else:
    print("Usage : %s %s %s %s %s %s %s" % (argv[0],'n','M','nk','u0','p','Msig'))
    exit()

#vectors to hold electron information 
#xx : Electron Position
xx = np.zeros(n*M)
#u : Electron Velocity
u = np.zeros(n*M)
#dx : Displacement in current turn
dx = np.zeros(n*M)

#I : Intensity of emitted light
I = []
#X : Electron Position
X = []
#V : Electron Velocity
V = []

for i in range(nk):
    #finding all those electrons whose position is greater than zero
    ii = np.where(xx>0)
    #updating the position and velocity of these electrons
    dx[ii] = u[ii] + 0.5
    xx[ii] += dx[ii]
    u[ii] += 1
    
    #all those electrons reached anode are stored in anode 
    anode = np.where(xx>=n)
    #the position and velocity of these electrons are set to zero
    xx[anode] = 0
    u[anode] = 0
    
    #kk is the vector of indices corresponding to energetic electrons with velocity greater than threshold velocity
    kk = np.where(u>=u0)[0]
    #creating a random vector and finding those entries that are less than or equal to p 
    ll = np.where(np.random.rand(len(kk))<=p)[0]
    #kl contains the indices of those energetic electrons that suffer a collision
    kl = kk[ll]
    
    #Setting the velocity of these electrons to zero (inelastic collision)
    u[kl] = 0
    #The collision could have occured at any point between previous xi and current xi
    xx[kl] -= dx[kl]*np.random.rand()
    
    #excited atoms at this location resulted in emmission from that point so adding a photon at this point and updating the I vector
    I.extend(xx[kl].tolist())
    
    #injecting m new electrons
    # this calculates the number injected this turn by rolling a random number, multiplying with standard deviation and adding the mean value
    m = int(np.random.rand()*Msig + M)
    #Finding the unused indices
    free_slots = np.where(xx == 0)[0]
    
    #if there are more slots than number of electrons then adding the electrons into the first m slots and setting their initial position and velocity
    if(len(free_slots) >= m):
        xx[free_slots[0:m]] = 1
        u[free_slots[0:m]] = 0
    #if there are lesser number of slots then adding to the available slots and initalising position and velocity
    else:    
        xx[free_slots] = 1
        u[free_slots] = 0
    
    #finding the active electrons
    active = np.where(xx>0)[0]
    #updating the X and V vectors with the position and velocity of active electrons
    X.extend(xx[active].tolist())
    V.extend(u[active].tolist())
    
#Electron Density Plot
plt.figure(0)
plt.hist(X,n,[0,n],ec='black')
plt.xlabel(r"x$\rightarrow$")
plt.ylabel(r'Number of Electrons$\rightarrow$')
plt.title("Electron Density")
plt.show()

#Light Intensity Plot
plt.figure(1)
ints,bins,trash = plt.hist(I,n,[0,n],ec='black')
plt.xlabel(r"x$\rightarrow$")
plt.ylabel(r'I$\rightarrow$')
plt.title("Light Intensity")
plt.show()

#Electron Phase Space
plt.figure(2)
plt.scatter(X,V,marker='x')
plt.xlabel(r"X$\rightarrow$")
plt.ylabel(r'V$\rightarrow$')
plt.title("Electron Phase Space")
plt.show()

#hist function returns three elements : array of population count, bin position, list of rectangles that are used to build up the histogram 
#The second element gives the dividing position between bins so has one dimension greater than the population array, so converting to midpoint values
xpos = 0.5*(bins[0:-1]+bins[1:])

#Tabulating the Intensity Data
d = [] 
[d.append([x,y]) for x, y in zip(xpos, ints)]
print("Intensity Data : \n")
print(tabulate((d),headers=['xpos', 'count']))
