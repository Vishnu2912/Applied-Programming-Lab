#	EE2703 : Applied Programming Lab
#	Endsem Assignment Jan - May 2021
#	Magnetic Field due to a current carrying loop
#Date : 30/5/2021
		
#Name : Vishnu Varma V
#Roll No : EE19B059

#Compilation : python3 EE19B059.py

#Pseudo code:

# 1.  Declare the limits to axes required for this problem 
#         0<x<2  0<y<2  1<z<1000
# 2.  Create Meshgrid to get points seperately in all three dimensions
# 3.  Initialize the variables
#         radius = 10cm
#         0 < phi < 2pi
# 4.  Create an array with x and y components 
#         x = radius*cos(phi); y = radius*sin(phi)
# 5.  Find the x and y components of the current elements corresponding to x and y coordinates
# 6.  Plot the loop and the current elements in the x-y plane
# 7.  Divide the loop into N = 100 parts
# 8.  dl is the small division which is a vector perpendicular to the loop 
#         dl_x = -k*sin(phi); dl_y = k*cos(phi)
#         k = 2pi*radius/N
# 9.  Function calc(): calculate vector potential for elemental length
#         Pass In: elemental section (0 to 99)
#         Calculate the distance between space points and the elemental length
#         Find the vector potential(A) corresponding to the elemental length
#         Pass Out: x and y components of A
#     EndFunction
# 10. Vector potential is divided into x and y component 
#         A_x = 0; A_y = 0 
# 11. for iteration = 0,1,...99 do
#         call the calc() function
#         summate the x component of vector potential obtained for elemental length 
#         summate the y component of vector potential obtained for elemental length
#     endfor
# 12. Calculate B using the vector potential components A_x and A_y
# 13. Fit B(z) to cz^(b) and obtain c and b using least squares method
# 14. Plot B vs z True value and the estimate obtained in loglog scale

#Code:

#Importing all the libraries required
import numpy as np
import matplotlib.pyplot as plt

#Initializing the space which we are considering to calculate the magnetic field
#x and y are varied from axis to 2cm on the positive axes
x = np.linspace(0,2,3)
y = np.linspace(0,2,3)
#while z is varied from 1cm to 1000cm this is the range in which Magnetic field is to be calculated
z= np.linspace(1,1000,1000)
#Using Meshgrid to get 3 arrays with one value fixed while the other two values varied 
X,Y,Z = np.meshgrid(x,y,z)

#radius given is 10cm
radius = 10
#Number of points to be considered on the circle is mentioned as 100
N = 100
#phi is the angle considered on the x-y plane which varies from 0 to 2pi
#N + 1 points are considered on the circle
phi = np.linspace(0,2*np.pi,N+1) 
#Last point is removed as 0 and 2*pi both are the same points
phi = phi[:-1]
#ro is the array with first row the x location as a function of phi i.e radius*cos(phi) and similarly y location as a function of phi i.e radius*sin(phi)
ro = np.array([radius*np.cos(phi),radius*np.sin(phi)])
#ro is replaced with its transpose now 1st column is x and second column y
ro = ro.T

#Plotting the circle using points denoted by ro with red dots
plt.figure(0)
plt.plot(ro[:,0],ro[:,1],'ro',label="wire loop")
#Providing title for the plot
plt.title("Loop of wire with radius 10cm")
#Providing x and y labels
plt.xlabel(r'$x(cm)\rightarrow$',size=14)
plt.ylabel(r'$y(cm)\rightarrow$',size=14)
#Enabling legend
plt.legend()
#Enabling grids
plt.grid()
#Displaying the plot
plt.show()

#declaring the permeability of free space
mu0 = 1.25663706e-6
#Finding the currents at particular x and y locations taken from ro[]
ix = -(4*np.pi/mu0)*np.cos(phi)*ro[:,1]
iy = (4*np.pi/mu0)*np.cos(phi)*ro[:,0]
#Plotting the quiver plot to show the magnitude and direction of current wrt x and y locations on the loop
plt.figure(1)
plt.quiver(ro[:,0],ro[:,1],ix,iy,label="Current Elements")
#Providing title for the plot
plt.title("Quiver plot of current")
#Providing x and y labels
plt.xlabel(r'$x(cm)\rightarrow$',size=14)
plt.ylabel(r'$y(cm)\rightarrow$',size=14)
#Enabling legend
plt.legend(loc='upper right')
#Enabling grids
plt.grid()
#Displaying the plot
plt.show()

#Dividing the loop into N parts using these points we can calculate the effect of each element on the vector potential
#dl is the elemental length perpendicular to the loop in the x-y plane
#First row contains the x component of that element of the loop and second row the y component
dl = (2*np.pi*radius/(N))*np.array([-np.sin(phi),np.cos(phi)])
#Now taking the transpose first column is x component and second column is y component
dl = dl.T

#Defining the function calc initially to calculate the distance between the point in space and the point on the loop so that its effect on the vector potential can be found
#Then calc() function is extended to generate the terms whose sum will lead to the x and y components of the vector potential
def calc(l):
    #R is the distance between the point in space(In this assignment we choose to take points in the proximity of the z axis from 1cm to 1000cm) and the points on the loop given by ro[]
    R = np.sqrt((X-ro[l,0])**2 + (Y-ro[l,1])**2 + (Z)**2) 
    #Reducing dl into x and y components
    dl_x =dl[l,0]
    dl_y =dl[l,1]
    #Generating vector potential corresponding to the x and y compenents of dl with other parameters corresponding to the elemental length being considered in the iteration of the for loop using the formula to calculate magnetic vector potential
    A_1 = np.cos(phi)[l]*np.exp(-0.1*1j*R)*dl_x/R
    A_2 = np.cos(phi)[l]*np.exp(-0.1*1j*R)*dl_y/R
    #Returning the vector potential A_1 and A_2 which are the x and y components of the vector potential corresponding to the elemental length considered
    return A_1,A_2

#Initializing the components of vector potential to 0
A_x = 0
A_y = 0
#Iterating through each element on the loop and finding the effect of that element on the vector potential
#Justification for using for loop: Even though we Vectorize this we need to use np.sum function to add them on an axis which internally uses a for loop, using both the methods we get almost same efficiency so we are using a for loop
for l in range(N):
    #calc function returns the x and y component of the vector potential corresponding to the elemental length being iterated
    A_1,A_2 = calc(l) 
    #Adding the vector potentials corresponding to elemental length in accordance with the principle of super position
    #Adding the x and y components of the vector potential respectively
    A_x  += A_1
    A_y  += A_2
#Calculating the Magnetic field using the magnetic vector potential, using the approximation of the curl of the vector potential
#The order of indices for vector potential is y,x,z 
B=(A_y[1,2,:]-A_x[2,1,:]-A_y[1,0,:]+A_x[0,1,:])/2
#Displaying the Maximum and Minimum values of the Magnetic Field
print("Maximum value of B :",max(abs(B)))
print("Minimum value of B :",min(abs(B)))
#Uncomment to print all the values of the magnetic field
#print(abs(B))
#Plotting the loglog plot of the magnetic field variation wrt z axis from 1cm to 1000cm
plt.figure(2)
plt.loglog(z,np.abs(B),'g-',label="Magnetic Field variation")
#Providing the tile for the plot
plt.title("Loglog plot of Magnetic field variation along z axis")
#Providing x and y labels
plt.xlabel(r'z$(cm)$$\rightarrow$',size=14)
plt.ylabel(r'$\vec{B}$(T)$\rightarrow$',size=14)
#Enabling legend
plt.legend()
#Enabling grids
plt.grid()
#Displaying the plot
plt.show()

#Fitting the magnetic field variation with z to an exponential and finding the exponent and multiplication factor
logB = np.log(abs(B))
param = np.zeros((len(B),2))
param[:,0] = 1
param[:,1] = np.log(z)
#Using least squares approach to find the unknowns
logc,b = np.linalg.lstsq(param,np.transpose(logB),rcond=None)[0]
c = np.exp(logc)
#Displaying the multiplication factor and exponent
print("c :",c)
print("b :",b)

#Estimating the magnetic field based on the least squares method
B_est = c*(z**b)
#Plotting the loglog plot of True value and Estimated value of B
plt.figure(3)
plt.loglog(z,np.abs(B),'g-',label="True Value")
plt.loglog(z,np.abs(B_est),'r-',label="Estimated Value")
#Providing title and x and y labels
plt.title("Estimated Magnetic field plot based on least squares")
plt.xlabel(r'$z(cm)$$\rightarrow$',size=14)
plt.ylabel(r'$\vec{B}$(T)$\rightarrow$',size=14)
#Enabling legend
plt.legend()
#Enabling grid
plt.grid()
#Displaying the plot
plt.show()
