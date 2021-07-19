	#EE2703 Assignment 5
#Name    : Vishnu Varma V
#Roll No : EE19B059

#importing all the required modules
import numpy as np
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.pyplot as plt
from sys import argv, exit

#if there are no inputs for parameters from commandline then setting them to the default values
if(len(argv) == 1):
    #Default values of parameters
    print("Using the default parameters Nx = 25, Ny = 25, radius = 8, Niter = 1500")
    Nx = 25
    Ny = 25
    radius = 8
    Niter = 1500
#if the parameter values are specified then allocating them respectively
elif(len(argv) == 5):
    Nx = int(argv[1])
    Ny = int(argv[2])
    radius = int(argv[3])
    Niter = int(argv[4])
#if neither of the case is satisfied then prompting the method to run the code
else:
    print("Usage : %s %s %s %s %s" % (argv[0],'Nx','Ny','radius','Niter'))
    exit()

#Function to fit exponential  
def exponential_fit(x,A,B):
    return A*np.exp(B*x)

#Function to get the parameters of the exponential
def error_fit(x_val,y_val):
    M = np.log(y_val)
    param = np.zeros((len(x_val),2))
    param[:,0] = 1
    param[:,1] = x_val
    logA,B = np.linalg.lstsq(param,np.transpose(M),rcond=None)[0]
    return (np.exp(logA),B)
    
#Function to find cumulative error    
def error_max(A,B,N):
    return -A*(np.exp(B*(N+0.5)))/B
        
#Defining the boundary on x and y axes with Ny and Nx points such that the zero is at the centre of the plate        
x = np.arange(Ny)-((Ny-1)/2)
y = np.arange(Nx)-((Nx-1)/2)
#Defining the potential function
phi = np.zeros((Ny,Nx))
#Defining the error function determined for each number of iterations
error = np.zeros(Niter)
#Meshgrid converts the given x and y points into two arrays one with x coordinates and the other with y coordinates with the same shape of the array
Y,X = np.meshgrid(y,x)
#Finding the points in the circle and storing in ii
ii = np.where((X*X + Y*Y) <= (radius)**2)
#Initialising the potential of all the points inside the circle to 1 V
phi[ii] = 1.0
xn,yn = ii

#Plotting the Inital contour of the potential 
#Opening a new figure
plt.figure(1)
#Marking the electrode via red dots
plt.plot(x[xn],y[yn],"ro")
#Plotting the contour
plt.contourf(Y,X,phi)
#Providing x and y labels
plt.xlabel(r'x$\rightarrow$',fontsize=15)
plt.ylabel(r'y$\rightarrow$',fontsize=15)
#Providing the title
plt.title("Initial Potential Configuration")
#Displaying the plot
plt.show()

for i in range(Niter):
    #python array is a pointer so using copy function to store in a new memory location
    oldphi = phi.copy()
    #updating the potential
    phi[1:-1,1:-1] = 0.25*(oldphi[1:-1,2:]+oldphi[1:-1,0:-2]+oldphi[2:,1:-1]+oldphi[0:-2,1:-1])
    #Boundary Conditions
    #Setting the open sides to the value from adjacent potential
    phi[1:-1,0] = phi[1:-1,1]
    phi[1:-1,-1] = phi[1:-1,-2]
    phi[0,1:-1] = phi[1,1:-1]
    #Ground side set to 0 potential
    phi[-1,1:-1] = 0
    #The potential within the circle is also modified so setting it back to 1 V
    phi[ii] = 1.0
    #Finding error in potential as a function of number of iterations
    error[i] = (abs(phi-oldphi)).max()
    
#Plotting the error function vs number of iterations on linear scale
plt.figure(2)
plt.plot(range(Niter),error,'-r',label='True Value')
plt.grid()
plt.xlabel(r'Niter$\rightarrow$')
plt.ylabel(r'Error$\rightarrow$')
plt.title('Error vs number of iterations in Linear Scale')
plt.show()

#Plotting the error function vs number of iterations on semilog scale
plt.figure(3)
#plotting every 50th point, to see individual data points
plt.semilogy(range(Niter),error,label='Error')
plt.semilogy(range(Niter)[::50],error[::50],'ro',label='50th data point')
plt.legend()
plt.grid()
plt.xlabel(r'Niter$\rightarrow$')
plt.ylabel(r'Error$\rightarrow$')
plt.title('Semilog plot of Error vs number of iterations')
plt.show()

#Plotting the error function vs number of iterations on loglog scale
plt.figure(4)
#plotting every 50th point, to see individual data points
plt.loglog(range(Niter),error,label='Error')
plt.loglog(range(Niter)[::50],error[::50],'ro',label='50th data point')
plt.legend()
plt.grid()
plt.xlabel(r'Niter$\rightarrow$')
plt.ylabel(r'Error$\rightarrow$')
plt.title('Loglog plot of Error vs number of iterations')
plt.show()

#Fitting an exponential to error obtained
#fit1 : for the entire vector of errors
A,B = error_fit(range(Niter),error)
#fit2 : for those error entries after the 500th iteration
A1,B1 = error_fit(range(Niter)[500:],error[500:])

#Plotting error fit1 and error fit2 along with the true error on loglog scale
plt.figure(5)
plt.loglog(range(Niter),error,'r',label='True Value')
plt.loglog(range(Niter)[::50],exponential_fit(range(Niter)[::50],A,B),'go',label='fit1')
plt.loglog(range(Niter)[::50],exponential_fit(range(Niter)[::50],A1,B1),'bo',label='fit2')
plt.legend(loc='upper right')
plt.grid()
plt.xlabel(r'Niter$\rightarrow$')
plt.ylabel(r'Error$\rightarrow$')
plt.title('Loglog plot of Error vs number of iterations')
plt.show()

#Plotting the cumulative error on a semilog scale
plt.figure(6)
#plotting every 50th, to see individual data points
plt.semilogy(range(Niter)[::50],error_max(A,B,np.arange(0,Niter,50)),'ro')
plt.grid()
plt.xlabel(r'Niter$\rightarrow$')
plt.ylabel(r'Cumulative Error$\rightarrow$')
plt.title('Semilog plot of Cumulative Error vs number of iterations')
plt.show()

#Surface Plot of Potential 
#open a new figure
fig = plt.figure(7)
#Axes3D is the means to do a surface plot
ax = p3.Axes3D(fig)
plt.title('The 3-D surface plot of the potential')
#plot_surface function does the plotting
surf = ax.plot_surface(Y, X, phi.T, rstride=1, cstride=1, cmap=plt.cm.jet)
plt.xlabel(r'x$\rightarrow$',fontsize=15)
plt.ylabel(r'y$\rightarrow$',fontsize=15)
ax.set_zlabel(r'$\phi\rightarrow$',fontsize=15)
plt.show()

#Plotting the Final contour of the potential 
plt.figure(8)
plt.plot(x[xn],y[yn],"ro")
plt.contourf(Y,X[::-1],phi)
plt.xlabel(r'x$\rightarrow$' , fontsize=15)
plt.ylabel(r'y$\rightarrow$',fontsize=15)
plt.title('Potential Configuration')
plt.show()

#Vector Plot of Currents
#Initialising the current density vectors
Jx = np.zeros((Ny,Nx))
Jy = np.zeros((Ny,Nx))
plt.figure(9)
#Numerical translation of the Current density and potential relation
Jx[:,1:-1] = 0.5*(phi[:,0:-2]-phi[:,2:])
Jy[1:-1,:] = 0.5*(phi[2:, :]-phi[0:-2,:])
#Plotting the Current density using quiver function
plt.quiver(Y[2:-1],X[::-1][2:-1],Jx[2:-1],Jy[2:-1],scale=5)
#Marking the electrode via red dots
plt.plot(x[xn],y[yn],"ro")
plt.title("The vector plot of the current flow")
plt.xlabel(r"x$\rightarrow$")
plt.ylabel(r'y$\rightarrow$')
plt.show()
