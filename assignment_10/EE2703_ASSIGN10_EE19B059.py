	#EE2703 Assignment 10
#Name    : Vishnu Varma V
#Roll No : EE19B059

#importing all the required modules
from pylab import *

#Defining the function which takes the parameters as inputs and gives the DFT spectrum as output
def spectrum(tl,N,func,wnd,xl,yl,i):
    #defining the time range given as input, taking N+1 points in this time range
    t=linspace(-tl,tl,N+1)
    #removing the last point as 0 and 2pi are the same
    t=t[:-1]
    #finding the difference between adjacent time samples
    dt=t[1]-t[0]
    fmax=1/dt
    #defining the range of w based on the sampling rate
    w=linspace(-pi,pi,N+1)*fmax
    #removing the last term to avoid overlap
    w=w[:-1]
    #Defining the function for which DFT is to be calculated
    y= func_dict[func](t)
    #if condition to decide whether to use windowing or not
    if (wnd == 1):
      #Defining the Hamming Window
      n=arange(N)
      wnd=fftshift(0.54+0.46*cos(2*pi*n/(N-1)))
      y=y*wnd
    y[0] = 0
    #shifting the function to center at 0 and taking the fft
    y=fftshift(y) 
    Y=fftshift(fft(y))/float(N)
    #Displaying a new figure
    figure(i)
    #Creating subplots to display both magnitude and phase spectrum
    subplot(2,1,1)
    #plotting the magnitude spectrum
    plot(w,abs(Y),'b',w,abs(Y),'bo',lw=2)    
    #providing the title for the plot
    title(title_dict[func])
    #limiting the axes for better visibility
    xlim([-xl,xl])
    #providing y label
    ylabel(r"$|Y|$",size=16)
    #Enabling the grid
    grid(True)
    subplot(2,1,2)
    #Plotting the phase spectrum
    plot(w,angle(Y),'ro',lw=2)
    #finding the indices of the points that have significant magnitude
    ii = where(abs(Y)>1e-3)
    #plotting these points in green
    plot(w[ii],angle(Y[ii]),'go',lw=2)
    #limiting x and y axes
    xlim([-xl,xl])
    ylim([-yl,yl])
    #providing x and y labels
    ylabel(r"Phase of $Y$",size=16)
    xlabel(r"$\omega$",size=16)
    #Enabling the grid
    grid(True)
    #Displaying the plot
    show()

#Defining the fucntions which we find the DFT for in this assignment and mapping them to the key through which the functions can be accessed
title_dict = {'cos': r"Spectrum of $cos^3(0.86t)$",'chirp': r"Spectrum of $cos(16t(1.5+\frac{t}{2\pi}))$"}
func_dict = {'cos':lambda t: cos(0.86*t)**3,'chirp' : lambda t : cos(16*t*(1.5+t/(2*pi)))}
#Finding the spectrum of cos^3(0.86t) without windowing
spectrum((4*pi),256,'cos',0,4,4,0)
#Finding the spectrum of cos^3(0.86t) with windowing
spectrum((4*pi),256,'cos',1,4,4,1)

#Defining the function to estimate the frequency and phase of the function based on the DFT
def estimate(tl,N,wnd,noise,wo,d,p,xl,yl,i):
    #defining the time range given as input, taking N+1 points in this time range
    t=linspace(-tl,tl,N+1)
    #removing the last point as 0 and 2pi are the same
    t=t[:-1]
    #finding the difference between adjacent time samples
    dt=t[1]-t[0]
    fmax=1/dt
    #defining the range of w based on the sampling rate
    w=linspace(-pi,pi,N+1)*fmax
    #removing the last term to avoid overlap
    w=w[:-1]
    #Defining the function for which DFT is to be calculated
    y= cos((wo*t)+d)
    #if condition to decide whether to use windowing or not
    if (wnd == 1):
      #Defining the Hamming Window
      n=arange(N)
      wnd=fftshift(0.54+0.46*cos(2*pi*n/(N-1)))
      y=y*wnd
    #if condition to decide whether to add noise or not
    if (noise == 1): 
      #white gaussian noice
      y = y + 0.1*np.random.randn(N)
    y[0] = 0
    #shifting the function to center at 0 and taking the fft
    y=fftshift(y) 
    Y=fftshift(fft(y))/float(N)
    #Displaying a new figure
    figure(i)
    #Creating subplots to display both magnitude and phase spectrum
    subplot(2,1,1)
    #plotting the magnitude spectrum
    plot(w,abs(Y),'b',w,abs(Y),'bo',lw=2) 
    #limiting the axes for better visibility   
    xlim([-xl,xl])
    #providing y label
    ylabel(r"$|Y|$",size=16)
    #providing title for the plot
    title("Spectrum of cos({}t+{})".format(wo,d))
    #Enabling the grid
    grid(True)
    subplot(2,1,2)
    #Plotting the phase spectrum of the function
    plot(w,angle(Y),'ro',lw=2)
    #finding the indices of the points that have significant magnitude
    ii = where(abs(Y)>1e-3)
    #plotting these points in green
    plot(w[ii],angle(Y[ii]),'go',lw=2)
    #limiting x and y axes
    xlim([-xl,xl])
    ylim([-yl,yl])
    #providing x and y labels
    ylabel(r"Phase of $Y$",size=16)
    xlabel(r"$\omega$",size=16)
    #Enabling the grid
    grid(True)
    #Displaying the plot
    show()
    #Finding those indices for which the frequency is positive
    kk  = where(w>=0)                                              
    #Taking one side of the spectrum 
    Y1,w1 = Y[kk],w[kk]                          
    #estimating wo using the weighted average of the first four points of the spectrum                      
    wo_est = sum(abs((Y1[:4]**p)*w1[:4]))/sum(abs(Y1[:4])**p)   
    #finding the indices of those points which have significant magnitude
    ll = where(abs(Y1) > 1e-4)[0]                          
    #estimating delta taking the mean of these phase points
    delta_est = mean(angle(Y1[ll[1:2]]))     
    if(noise == 1):
        print("With Noise")
    else:
        print("Without Noise")
    #Printing the estimated values
    print("Estimated wo : {}".format(wo_est))
    print("Estimated delta : {}".format(delta_est))
    #Printing the error in estimated values
    print("Error in estimate of wo: {}".format(abs(wo-wo_est)))
    print("Error in estimate of delta : {}".format(abs(d-delta_est)))

#Estimating frequency and phase of cos((wo*t)+delta) without adding noise    
estimate(pi,128,1,0,0.8,1,1,4,4,4)
#Estimating frequency and phase of cos((wo*t)+delta) adding noise    
estimate(pi,128,1,1,0.8,1,1,4,4,5)

#Finding the spectrum of the chirped signal without windowing
spectrum(pi,1024,'chirp',0,50,4,2)
#Finding the spectrum of the chirped signal with windowing
spectrum(pi,1024,'chirp',1,50,4,3)

#Defining the function to obtain the DFT of the chirped Signal
def chirp_spectrum(t1,N,func,wnd,xl,yl,i):
    #time range for each duration of 64 samples
    t=linspace(t1[0],t1[-1],N+1)
    #removing the last point
    t=t[:-1]
    #finding the difference between adjacent time samples
    dt=t[1]-t[0]
    fmax=1/dt
    #defining the range of w based on the sampling rate
    w=linspace(-pi,pi,N+1)*fmax
    #removing the last term to avoid overlap
    w=w[:-1]
    #Defining the function for which the DFT is to be calculated
    y= func_dict[func](t)
    #if condition to decide whether to use windowing or not
    if (wnd == 1):
      #Defining the Hamming Window
      n=arange(N)
      wnd=fftshift(0.54+0.46*cos(2*pi*n/(N-1)))
      y=y*wnd
    y[0] = 0
    #shifting the function to center at 0 and taking the fft
    y=fftshift(y) # make y start with y(t=0)
    Y=fftshift(fft(y))/float(N)
    #returning the DFT of the function and frequency 
    return Y,w

#t1 is the the time range with 1024 samples
t1 = linspace(-pi,pi,1025)
#removing the last term
t1 = t1[:-1]
#Initialising the Y_chirp 2D array with zeros and type complex
Y_chirp = np.zeros((16,64),dtype = 'complex_')
#Iterating through each part of the time range, break the 1024 vector into pieces that are 64 samples wide so there would be 16 such pieces iterating through them
for i in range(16):
  #passing the parameters to obtain the DFT of the chirped signal
  Y,w = chirp_spectrum(t1[64*i:64*(i+1)],64,'chirp',1,50,4,3)
  #storing the DFT correspoding to each piece as a column in a 2D array
  Y_chirp[i][:] = Y                                    

#obtaining the points after breaking the vector into 64 samples wide.
t1 = t1[::64]
#using meshgrid for the surface plot
t1,w = meshgrid(t1,w)

#Plotting the magnitude spectrum with t and w as a surface plot
fig_m = figure(6)                                                                
ax =  axes(projection ='3d')      
#Providing title                                                  
ax.set_title('The 3D surface plot of $|Y|$', fontsize = 14)             
#Providing x and y label                                   
ax.set_xlabel(r'$\leftarrow$ w $\rightarrow$', fontsize = 12)                        
ax.set_ylabel(r'$\leftarrow$ t $\rightarrow$', fontsize = 12)                     
#plotting the surface plot     
surf = ax.plot_surface(w, t1, abs(Y_chirp.T),cmap = cm.rainbow, rstride=1, cstride=1)
#Displaying the colorbar
fig_m.colorbar(surf, ax = ax,shrink = 0.5, aspect = 5)                     
#Displaying the plot           
show()

#Plotting the Phase spectrum with t and w as a surface plot
fig_m = figure(7)                                                                
ax =  axes(projection ='3d')          
#Providing title                                                                                                
ax.set_title('The 3D surface plot of Phase of $Y$', fontsize = 14)
#Providing x and y label                                                
ax.set_xlabel(r'$\leftarrow$ w $\rightarrow$', fontsize = 12)                        
ax.set_ylabel(r'$\leftarrow$ t $\rightarrow$', fontsize = 12)  
#Plotting the surface plot                        
surf = ax.plot_surface(w, t1, angle(Y_chirp.T),cmap = cm.rainbow, rstride=1, cstride=1)
#Displaying the colorbar
fig_m.colorbar(surf, ax = ax,shrink = 0.5, aspect =  5)
#Displaying the plot
show()

