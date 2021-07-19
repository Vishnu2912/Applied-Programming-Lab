	#EE2703 Assignment 7
#Name    : Vishnu Varma V
#Roll No : EE19B059

#importing all the modules required
import numpy as np
import scipy.signal as sp
import matplotlib.pyplot as plt

#defining the function to take the frequency and decay as input and produce the Numerator and Denominator of Transfer function as output
def Transfer(w,a):
    p1 = np.poly1d([1,w])
    p2 = np.poly1d([1,(2*w),((w*w)+(a*a))])
    return p1,p2
   
#Spring System
#Numerator and Denominator of the Transfer function obtained using the function defined
n1,d1 = Transfer(0.5,1.5)
#The denominator is multiplied to get the Laplace expression of X(s)
d1 = np.polymul(d1,[1,0,2.25])
#passing the numerator and denominator to sp.lti
H1 = sp.lti(n1,d1)
t = np.linspace(0,50,1000)
#Finding the impulse response of H1
t,x = sp.impulse(H1,None,t)
#Plotting the Time Response
plt.figure(0)
plt.plot(t,x,label='Decay = 0.5')
plt.legend(loc='upper left')
plt.grid()
plt.xlabel(r"t$\rightarrow$")
plt.ylabel(r'x$\rightarrow$')
plt.title("Time response of Spring for decay = 0.5")
plt.show()

#Spring System with smaller Decay
#Following the same method for a smaller decay
n2,d2 = Transfer(0.05,1.5)
d2 = np.polymul(d2,[1,0,2.25])
H2 = sp.lti(n2,d2)
t = np.linspace(0,50,1000)
t,x = sp.impulse(H2,None,t)
#Plotting the Time response for smaller decay
plt.figure(1)
plt.plot(t,x,label='Decay = 0.05')
plt.legend(loc='upper left')
plt.grid()
plt.xlabel(r"t$\rightarrow$")
plt.ylabel(r'x$\rightarrow$')
plt.title("Time response of Spring for decay = 0.05")
plt.show()

#Response for varying frequency 
i = 0 
plt.figure(2)
#finding the time response for frequency varying from 1.4 to 1.6 in steps of 0.05
for f in np.arange(1.4,1.6,0.05):
    H = sp.lti([1],[1,0,2.25])
    t1 = np.linspace(0,100,1000)
    x1 = np.cos(f*t1)
    x2 = np.multiply(np.exp(-0.05*t1),np.heaviside(t1,0.5))
    func1 = np.multiply(x1,x2)
    #Convolving func1 and H
    t,x,_ = sp.lsim(H,func1,t1)
    i +=1
    #Plotting all the plots in a single figure using subplot
    plt.subplot(3,2,i)
    #Labeling the frequency corresponding to each plot
    plt.plot(t1,x,label='f =%.2f'%f)
    plt.grid()
    plt.legend(loc='upper left',fontsize=8)
plt.show()
    
# Coupled spring system
t = np.linspace(0,20,1000)
#Defining X(s) and Y(s) obtained from the coupled equations given
X_s = sp.lti(np.poly1d([1,0,2]),np.poly1d([1,0,3,0]))
#Finding the impulse response of x(t) and y(t)
t,x = sp.impulse(X_s,None,t)
Y_s = sp.lti(np.poly1d([2]),np.poly1d([1,0,3,0]))
t,y = sp.impulse(Y_s,None,t)
#Plotting x(t) and y(t)
plt.figure(3)
plt.plot(t,x,label='$x(t)$')
plt.plot(t,y,label='$y(t)$')
plt.legend()
plt.grid()
plt.xlabel(r"t$\rightarrow$")
plt.ylabel('$x(t)$,$y(t)$')
plt.title("Solution of $x(t)$ and $y(t)$ of coupled spring")
plt.show()

#Two port Network
#Defining the Transfer function obtained from the given circuit
H = sp.lti(np.poly1d([1e12]),np.poly1d([1,1e8,1e12]))
#finding the bode Magnitude and Phase
w,S,phi = H.bode()
#Plotting the Magnitude and Phase response of the Transfer Function
plt.figure(4)
plt.subplot(2,1,1)
plt.semilogx(w,S)
plt.grid()
plt.title("Magnitude and phase response of $H(s)$")
plt.xlabel('$w$')
plt.ylabel(r'$|H(s)|$')
plt.subplot(2,1,2)
plt.semilogx(w,phi)
plt.grid()
plt.xlabel('$w$')
plt.ylabel(r'$\angle(H(s))$')
plt.show()

#for t varying in micro seconds
t = np.linspace(0,30*(1e-6),1000)
#The given input voltage vi(t)
vi = np.multiply(np.cos(1000*t)-np.cos(1000000*t),np.heaviside(t,0.5))
#convolving vi with H gives the output voltage
t,vo1,vsec = sp.lsim(H,vi,t)
#Plotting the output voltage for 0<t<30 microseconds
plt.figure(5)
plt.plot(t,vo1)
plt.grid()
plt.xlabel(r"t$\rightarrow$")
plt.ylabel(r'$v_{o}(t)$$\rightarrow$')
plt.title("Output voltage $v_o(t)$ for 0<t<30$\mu$s")
plt.show()

#for t varying in milli seconds
t = np.linspace(0,10*0.001,100000)
vi = np.multiply(np.cos(1000*t)-np.cos(1000000*t),np.heaviside(t,0.5))
#followng the same procedure but now for different time sample
t,vo2,svec = sp.lsim(H,vi,t)
#Plotting the output voltage for 0<t<10ms
plt.figure(6)
plt.plot(t,vo2)
plt.grid()
plt.xlabel(r"t$\rightarrow$")
plt.ylabel(r'$v_{o}(t)$$\rightarrow$')
plt.title("Output voltage $v_o(t)$ for 0<t<10ms")
plt.show()
