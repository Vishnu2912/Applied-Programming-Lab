	#EE2703 Assignment 3
#Name    : Vishnu Varma V
#Roll No : EE19B059

#importing all the modules required for this program
import numpy as np
import scipy.special as sp
import matplotlib.pyplot as plt

#Defining the function g(t)
def g(t,A,B):
	return A*sp.jn(2,t) + B*t

#Extracting data from fitting.dat
#matrix to store the data from fitting.dat
data_c = []
data_c = np.loadtxt('fitting.dat', dtype = float)
#the first column of fitting.dat is time 
time = np.array(data_c[:,0])
#starting from the second column all the colums are data 
y_col = np.asarray(data_c)[:,1:]
#noise is normally distributed with std deviation sigma
sigma = np.logspace(-1,-3,9)

#Plotting the Data to be fitted to theory
plt.figure()
#parsing through the 9 other columns apart from time and plotting them
for i in range(9):
	#x axis is time and y axis is the data given for each sigma respectively
	plt.plot(time,y_col[:,i],label = r'$\sigma$=%.3f'%sigma[i])
#Plotting the true curve without any noise using the function definition	
plt.plot(time,g(time,1.05,-0.105),label = 'True Curve')
#Giving the title to the plot
plt.title(r'Q4: Data to be fitted to theory')
#legend specifies the analogy between plot and corresponding sigma in this plot
plt.legend()
#ylabel is the function which we are plotting with respect to xlabel and specifying their font size
plt.ylabel(r'f(t)+noise$\rightarrow$',fontsize=15)
plt.xlabel(r't$\rightarrow$',fontsize=15)
#show function displays the plot
plt.show()

#Errorbar Plot
#accessing the first column of data to plot error bar
data = y_col[:,0]
#every fifth data item is plotted to make the plot readable first column corresponds to sigma[0]
plt.errorbar(time[::5],data[::5],sigma[0],fmt='ro',label='Errorbar')
#Plotting the true curve without any noise using the function definition
plt.plot(time,g(time,1.05,-0.105),'b',label='$f(t)$')
#Giving the title to the plot
plt.title('Q5: Data points for $\sigma$ = '+ str(sigma[0]) +' along with exact function')
#legend appears in the upper right portion of the plot
plt.legend(loc='upper right')
plt.xlabel(r't$\rightarrow$',fontsize=15)
plt.show()

#constructing the matrix M
fn_column = sp.jn(2,time)
M = np.c_[fn_column,time]
#known parameters to verify if both give the same answer
A = 1.05; B = -0.105
C = np.array([A,B])
#g_mul is obtained by multipying M and C
g_mul = np.matmul(M,C)
#g_func is obtained by the function definition
g_func = np.array(g(time,A,B))
#comparing g_mul and g_func to check if they both are equal
print("The vectors obtained from matrix multiplication and by function definition are equal : ",np.array_equal(g_mul,g_func))

#The Error Function
#e is the error function 
e = np.zeros((21,21,9))
#A is the first parameter
A = np.linspace(0,2,21)
#B is the second parameter
B = np.linspace(-0.2,0,21)
#parsing through each line of data to find error for each data point
for k in range(9):
	f = y_col[:,k]
	for i in range(21):
		for j in range(21):
			e[i][j][k] = np.sum((f -np.array(g(time,A[i],B[j])))**2)/101

#Contour Plot
#plotting a contour plot of error function
plot = plt.contour(A,B,e[:,:,0],20)
plt.title('Q8: Contour plot of $\epsilon_{ij}$')
plt.ylabel(r'B$\rightarrow$')
plt.xlabel(r'A$\rightarrow$')
plt.clabel(plot,inline=1,fontsize=10)
#unravel function of numpy module is used to get the loaction of minimum
#argmin function of numpy module returns the index of minima for the flattened array
a = np.unravel_index(np.argmin(e[:,:,0]),e[:,:,0].shape)
#locating the points exact location and location at which it is minimum
plt.plot(A[a[0]],B[a[1]],'o',markersize=3, label = 'Minimum Location')
plt.plot(1.05,-0.105,'ro',markersize=3, label = 'Exact Loacation')
plt.legend()
plt.show()

#Least mean square estimation
#linear scale 
#est calculated using numpy function lstsq for 9 columns of data available
estimate = [np.linalg.lstsq(M,y_col[:,i],rcond=None)[0] for i in range(9)]
#The asarray() function is used to convert a given input to an array
estimate = np.asarray(estimate)
#we know the actual parameters so calculating the absolute difference between them
#error_a is error in estimation of parameter A
error_a = abs(estimate[:,0]-1.05)
#error_b is error in estimation of parameter B
error_b = abs(estimate[:,1]+0.105)
#error in parameter estimation is plotted against sigma 
plt.plot(sigma,error_a,'ro--',label='A_err')
plt.plot(sigma,error_b,'go--',label='Berr')
plt.title('Q10: Variation of error with noise')
plt.ylabel(r'$MS$ $Error$$\rightarrow$',fontsize=15)
plt.xlabel(r'$\sigma_{n}\rightarrow$',fontsize=15)
plt.legend(loc='upper left')
plt.show()

#logscale
plt.figure()
#A stem plot plots vertical lines at each x location from the baseline to y
plt.stem(sigma,error_a,'-ro')
plt.stem(sigma,(error_b),'-go')
#plotting the error in parameter estimation in loglog scale
plt.loglog(sigma,error_a,'ro')
plt.loglog(sigma,error_b,'go')
plt.title('Q11: Variation of error with noise')
plt.xlabel(r'$\sigma_{n}\rightarrow$',fontsize=15)
plt.ylabel(r'$MS$ $Error$$\rightarrow$',fontsize=15)
plt.show()

