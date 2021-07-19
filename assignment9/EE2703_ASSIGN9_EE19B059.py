	#EE2703 Assignment 9
#Name    : Vishnu Varma V
#Roll No : EE19B059

#importing all the modules required 
from pylab import *

#Defining the fucntions which we find the DFT for in this assignment and mapping them to the key through which the functions can be accessed
title_dict = {'cos': r"Spectrum of $cos^3(t)$",'sin': r"Spectrum of $sin^3(t)$",'fm': r"Spectrum of $cos(20t+5cos(t))$"}
func_dict = {'cos' : lambda x : cos(x)**3,'sin' : lambda x : sin(x)**3,'fm' : lambda x : cos(20*x+5*cos(x))}
#Defining the function we use to find and plot DFT's with the signal and other parameters as input
def spectrum(func,N,wl,tl,xl,i):
	#the timespace is linear and the limit for it, and the number of points to be considered are the parameters obtained 
	#in general -tl and tl are the same points, so we have to stop just before the last term so the last term is dropped 
	t=linspace(-tl,tl,(N+1));t=t[:-1]
	#the signal obtained as a parameter is converted back to the actual signal and assigned to y
	y= func_dict[func](t)
	#Now finding the DFT of this signal and dividing by the number of sample points
	Y = fftshift(fft(y))/N
	#Defining the frequency limits and the number of points to be considered
	w=linspace(-wl,wl,(N+1))
	w = w[:-1]
        #Displaying a new figure
	figure(i)
	#Plotting both magnitude and phase spectrum so using subplots
	subplot(2,1,1)
	#Plotting the magnitude spectrum
	plot(w,abs(Y),lw=2)
	#Displaying the part of the axis which we would like to focus on
	xlim([-xl,xl])
	title(title_dict[func])
	#labelling the axis
	ylabel(r"$|Y|$",size=16)
	#Enabling grids in the plot
	grid(True)
	subplot(2,1,2)
	#We require all the phase points only for sinusoids and for other only the phase points with magnitude greater than a particular magnitude
	if func == 'cos' or func == 'sin' or func == 's':
		plot(w,angle(Y),'ro',lw=2)
	#collecting the points with phase points greater than the required magnitude	
	ii = where(abs(Y)>1e-3)
	#plotting those phase points 
	plot(w[ii],angle(Y[ii]),'go',lw=2)
	#Displaying the part of the axis which we would like to focus on
	xlim([-xl,xl])
	#labelling the axes
	ylabel(r"Phase of $Y$",size=16)
	xlabel(r"$\omega$",size=16)
	#Enabling grids in the plot
	grid(True)
	#Displaying the plots
	show()
#Callling the function to plot magnitude and phase spectrum for the signals 
spectrum('sin',256,64,2*pi,10,0)
spectrum('cos',256,64,2*pi,10,1)
spectrum('fm',512,64,4*pi,50,2)

#To find out the time range for which the frequency domain spectrum accurate to 6 digits
#Initializing tl to pi and N to 256
tl = pi
N = 256
#Iterating 20 times because if the fft does not converge then to terminate at 20 iterations
for i in range(20):
	t = linspace(-tl,tl,N+1)
	t = t[:-1]
	wl = pi*(N/(2*tl))
	w = linspace(-wl,wl,N+1)
	w = w[:-1]
	#The estimated and expected dft of the gaussian 
	Y = fft(ifftshift(exp(-t**2/2)))
	Y = fftshift(Y)*((2*tl)/N)
	Y_exp = sqrt(2*pi)*exp(-(w**2)/2)
	#Finding the error between them
	error = max(abs(Y-Y_exp))
	#If the error is accurate to 6 digits then taking the time range corresponding to it
	if(error < 1e-6):
		tl_final = tl
		error_final = error
		break
	#Incrementing the time range for every iteration
	tl += pi
#Displaying the time range for which the dft is accurate to 6th digit
print("For N = {} : error = {} and time limit = {:.4f}".format(N,error_final,tl_final))

#For Gaussian the following method is used
#tl is the time range
#N is the number of samples
#xl and yl are the x and y limits to display in the figure respectively
def gaussian(tl,N,xl,yl,i):
	t = linspace(-tl,tl,N+1)
	t = t[:-1]
	#2*tl is the complete time range 
	w = linspace(-pi,pi,N+1)*N/(2*tl)
	w = w[:-1]	
	figure(i)
	subplot(2,1,1)
	#Y is the fft of the gaussian we are estimating
	Y = fft(ifftshift(exp(-t**2/2)))
	Y = fftshift(Y)*((2*tl)/N)
	#Y_exp is the expected fft of the gaussian
	Y_exp = exp(-w**2/2)*sqrt(2*pi)
	#Displaying the error between the estimated and expected gaussian
	print("Error for t limit = {:.4f}, N = {}, is {}".format(tl,N,max(abs(Y_exp - Y))))
	#Plotting the magnitude and phase response under given x limit and y limit
	plot(w,abs(Y),lw = 2)
	xlim([-xl,xl])
	ylabel(r"$|Y|$",size=16)
	title(r"Spectrum of $\exp(-t^2/2)$ tl = {:.3f}, N = {}".format(tl,N))
	grid(True)
	subplot(2,1,2)
	ii = where(abs(Y)>1e-3)
	plot(w[ii],angle(Y[ii]),'go',lw =2)
	xlim([-xl,xl])
	ylim([-yl,yl])
	ylabel(r"Phase of $Y$",size=16)
	xlabel(r"$\omega$",size=16)         
	grid(True)     
	show()

#Finding the fft of gaussian for tl = 2*pi and N = 256 and 512
gaussian(2*pi,256,15,4,3)
gaussian(2*pi,512,15,4,4)


