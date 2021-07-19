	#EE2703 Assignment 4
#Name    : Vishnu Varma V
#Roll No : EE19B059

#importing all the modules required for this program
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad
import scipy

#defining exponential function
def exp(x):
	return np.exp(x)
#defining cos(cos(x)) function
def ccos(x):
	return np.cos(np.cos(x))

#Taking 300 points between -2pi to 4pi
x = np.linspace(-2*np.pi,4*np.pi,300)
#The fundamental period being 2pi taking 100 points between them
xtile = np.linspace(0,2*np.pi,100)
#Tile function repeates values from 0 to 2pi 3 times to constitute from -2pi to 4pi
tiled = np.tile(xtile,3)
exp_x = exp(x)
ccos_x = np.cos(np.cos(x))
#Plotting exp(x) on semilogy 
#the graph in red colour is the Actual plot without any periodicity
plt.semilogy(x,exp_x,'r', label = 'Actual value')
#To calculate the fourier series exp(x) is periodically extended plotted in blue colour
plt.semilogy(x,exp(tiled),'-b',label='Periodic extension')
#allowing grids
plt.grid(True)
#Labelling x and y axis
plt.ylabel(r'$e^{x}\rightarrow$',fontsize=15)
plt.xlabel(r'x$\rightarrow$',fontsize=15)
#Giving Title
plt.title('Semilog plot of $e^{x}$',fontsize=15)
#Displaying the legend on upper right corner
plt.legend(loc='upper right')
#Displaying the plot
plt.show()

#cos(cos(x)) is plotted in linear scale
plt.plot(x,ccos_x,'b')
#allowing grids providing x, y labels and title
plt.grid(True)
plt.xlabel(r'x$\rightarrow$',fontsize=15)
plt.ylabel(r'$\cos(\cos(x))\rightarrow$',fontsize=15)
plt.title('Plot of $\cos(\cos(x))$',fontsize=15)
plt.show()

#To calculate fourier coefficients
#Arguments are the number of coefficients required(including a[0] a[n] and b[n]) and the function name in our case exp and ccos
def fourier_coef(n,func):
    #Declaring the vector with fourier coefficients 
    coef = np.zeros(n)
    #u and v are the functions obtained by multiplying the given function with cos and sin respectively
    #lambda function can take any number of arguments, but can only have one expression.
    u = lambda x,k: func(x)*np.cos(k*x)
    v = lambda x,k: func(x)*np.sin(k*x)
    #Calculating a[0]
    coef[0]= quad(func,0,2*np.pi)[0]/(2*np.pi)   
    #Calculating a[n] and b[n] using the formula
    for i in range(1,n,2): 
        coef[i] = quad(u,0,2*np.pi,args=((i+1)/2))[0]/np.pi
    for i in range(2,n,2):
        coef[i] = quad(v,0,2*np.pi,args=(i/2))[0]/np.pi
    return coef
    
#Passing the arguments to find the fourier coefficients
#coef_exp contains first 51 fourier coefficients of exp(x)
coef_exp = fourier_coef(51,exp)
#coef_cos contains first 51 fourier coefficients of cos(cos(x))
coef_cos = fourier_coef(51,ccos)

#plotting the fourier coefficients of exp(x) in semilog scale
plt.semilogy(range(51),np.abs(coef_exp),'ro')
plt.grid(True)
plt.xlabel(r'n$\rightarrow$',fontsize=15)
plt.ylabel(r'Coefficient Magnitude$\rightarrow$',fontsize=15)
plt.title('Semilog Plot of coefficients for $e^{x}$',fontsize=15)
plt.show()

#plotting the fourier coefficients of exp(x) in loglog scale
plt.loglog(range(51),np.abs(coef_exp),'ro')
plt.grid(True)
plt.xlabel(r'n$\rightarrow$',fontsize=15)
plt.ylabel(r'Coefficient Magnitude$\rightarrow$',fontsize=15)
plt.title('Loglog Plot of coefficients of $e^{x}$',fontsize=15)
plt.show()

#plotting the fourier coefficients of cos(cos(x)) in semilog scale
plt.semilogy(range(51),abs(coef_cos),'ro')
plt.grid(True)
plt.xlabel(r'n$\rightarrow$',fontsize=15)
plt.ylabel(r'Coefficient Magnitude$\rightarrow$',fontsize=15)
plt.title('Semilog Plot of coefficients for $cos(cos(x))$',fontsize=15)
plt.show()

#plotting the fourier coefficients of cos(cos(x)) in loglog scale
plt.loglog(range(51),abs(coef_cos),'ro')
plt.grid(True)
plt.xlabel(r'n$\rightarrow$',fontsize=15)
plt.ylabel(r'Coefficient Magnitude$\rightarrow$',fontsize=15)
plt.title('Loglog Plot of coefficients of $cos(cos(x))$',fontsize=15)
plt.show()

#Taking 401 points between 0 to 2pi
x = np.linspace(0,2*np.pi,401)
#To have a periodic integral last term is dropped
x = x[:-1]
#Declaring A matrix with 400 rows and 51 columns
A = np.zeros((400,51))
#The first column of the matrix is 1 due to the fourier series definition
A[:,0] = 1
for k in range(1,26):
    A[:,2*k-1] = np.cos(k*x)      #cos(kx) column
    A[:,2*k] = np.sin(k*x)        #sin(kx) column 
#B_exp and B_cos are the vectors with the true function values 
B_exp = exp(x)  
B_cos = np.cos(np.cos(x))
#this will find out the best fit numbers that will satisfy c_exp and c_cos respectively matrix
c_exp = scipy.linalg.lstsq(A,B_exp)[0]
c_cos = scipy.linalg.lstsq(A,B_cos)[0]

#Plotting the absolute values obtained by least squares method and the function definition for exp(x) on semilog scale  
plt.semilogy(range(51),np.abs(c_exp),'go',label="Using Least Squares")
plt.semilogy(range(51),np.abs(coef_exp),'ro',label='True Value',markersize=4)
plt.grid(True)
plt.xlabel(r'n$\rightarrow$',fontsize=15)
plt.ylabel(r'Coefficient Magnitude$\rightarrow$',fontsize=15)
plt.title('Semilog Plot of coefficients for $e^{x}$',fontsize=15)
plt.legend(loc='upper right')
plt.show()

#Plotting the absolute values obtained by least squares method and the function definition for exp(x) on loglog scale
plt.loglog(range(51),np.abs(c_exp),'go',label="Using Least Squares")
plt.loglog(range(51),np.abs(coef_exp),'ro',label = 'True Value',markersize=4)
plt.grid(True)
plt.xlabel(r'n$\rightarrow$',fontsize=15)
plt.ylabel(r'Coefficient Magnitude$\rightarrow$',fontsize=15)
plt.title('Loglog Plot of coefficients of $e^{x}$',fontsize=15)
plt.legend(loc='lower left')
plt.show()

#Plotting the absolute values obtained by least squares method and the function definition for cos(cos(x)) on semilog scale
plt.semilogy(range(51),abs(c_cos),'go',label="Using Least Squares")
plt.semilogy(range(51),abs(coef_cos),'ro',label='True value',markersize=4)
plt.grid(True)
plt.xlabel(r'n$\rightarrow$',fontsize=15)
plt.ylabel(r'Coefficient Magnitude$\rightarrow$',fontsize=15)
plt.title('Semilog Plot of coefficients for $cos(cos(x))$',fontsize=15)
plt.legend(loc='upper right')
plt.show()

#Plotting the absolute values obtained by least squares method and the function definition for cos(cos(x)) on loglog scale
plt.loglog(range(51),abs(c_cos),'go',label="Using Least Squares")
plt.loglog(range(51),abs(coef_cos),'ro',label='True value',markersize=4)
plt.grid(True)
plt.xlabel(r'n$\rightarrow$',fontsize=15)
plt.ylabel(r'Coefficient Magnitude$\rightarrow$',fontsize=15)
plt.title('Loglog Plot of coefficients of $cos(cos(x))$',fontsize=15)
plt.legend(loc='upper right')
plt.show()

#absolute difference between the two sets of coefficients
dev_exp = abs(coef_exp - c_exp)
dev_cos = abs(coef_cos - c_cos)

#Finding the largest deviation
max_dev_exp = np.max(dev_exp)
max_dev_cos = np.max(dev_cos)
#Displaying the largest deviation in each case
print("Maximum Deviation in exp(x) = ", max_dev_exp)
print("Maximum Deviation in cos(cos(x)) = ", max_dev_cos)

#Computing Ac from the estimated values of c 
est_exp = np.matmul(A,c_exp)
est_ccos = np.matmul(A,c_cos)
#plotting estimated and actual functional values 
plt.semilogy(x,est_exp,'go',label="Function Approximation")
plt.semilogy(x,exp(x),'-r',label='True value')
plt.grid(True)
plt.xlabel(r'n$\rightarrow$',fontsize=15)
plt.ylabel(r'$f(x)\rightarrow$',fontsize=15)
plt.title('Plot of $e^{x}$ and its Fourier series approximation',fontsize=15)
plt.legend(loc='lower right')
plt.show()

#plotting estimated and actual functional values 
plt.plot(x,est_ccos,'go',label="Function Approximation")
plt.plot(x,np.cos(np.cos(x)),'-r',label='True value')
plt.grid(True)
plt.xlabel(r'n$\rightarrow$',fontsize=15)
plt.ylabel(r'$f(x)\rightarrow$',fontsize=15)
plt.title('Plot of $cos(cos(x))$ and its Fourier series approximation',fontsize=15)
plt.legend(loc='upper right')
plt.show()
