	#EE2703 Assignment 8
#Name    : Vishnu Varma V
#Roll No : EE19B059

#importing all the modules required
import numpy as np 
from sympy import *
import scipy.signal as sp 
import os 
import warnings 
warnings.filterwarnings("ignore")
init_session
import matplotlib.pyplot as plt
    
#Defining the function to convert the given Sympy Transfer function to Scipy
def converter(Vo):
    #Splitting the Transfer function into numerator and denominator
    num, den = simplify(Vo).as_numer_denom()  
    p_num_den = poly(num, s), poly(den, s)
    #Returning the coefficients of the polynomials
    c_num_den = [p.all_coeffs() for p in p_num_den] 
    l_num, l_den = [lambdify((), c)() for c in c_num_den]
    #returning the Scipy LTI 
    return sp.lti(l_num, l_den)
        
#Defining the lowpass Filter
def lowpass(R1,R2,C1,C2,G,Vi):
    #s is the complex variable used
    s=symbols('s')
    #Defining A and b matrices obtained from circuit analysis
    A=Matrix([[0,0,1,-1/G],[-1/(1+s*R2*C2),1,0,0],[0,-G,G,1],[-1/R1-1/R2-s*C1,1/R2,0,s*C1]])
    b=Matrix([0,0,0,-Vi/R1])
    #Obtainig the Voltage matrix using A and b
    V = A.inv()*b
    return (A,b,V)

#Step response of lowpass filter
#s is the complex variable used
s = symbols('s')
#Obatining A,b,V using the function defined
A,b,V=lowpass(10000,10000,1e-9,1e-9,1.586,1)
#The fourth element of V matrix is the output voltage
Vo = V[3]
#Converting the sympy Transfer function to Scipy LTI
H = converter(Vo)
t = np.linspace(0,0.001,10000)
#Obtaining the step response
t,y = sp.step(H,T=t)
#Plotting the Step response
plt.figure(0)
plt.plot(t,y)
plt.xlabel("$t$")
plt.ylabel("$V_{o}$")
plt.title("Step response of Low pass Filter")
plt.grid(True)
plt.show()

#Mixed frequency sinusoid as Input
t = np.linspace(0,0.01,100000)
#Input Voltage
Vi = np.multiply((np.sin(2000*np.pi*t)+np.cos(2000000*np.pi*t)),np.heaviside(t,0.5))
#Convolving H and Vi to get Vo
Vo = sp.lsim(H,Vi,t)
#Plotting the Voltage for Mixed frequency sinusoidal input
plt.figure(1)
#Plotting Vi vs t
plt.plot(Vo[0],Vi,label="$V_{i}$")
#Plotting Vo vs t
plt.plot(Vo[0],Vo[1],label="$V_{o}$")
plt.xlabel("$t$")
plt.ylabel("$V$")
plt.legend(loc ='upper right')
plt.title("$V_o$ for mixed frequency sinusoid as $V_i$")
plt.grid(True)
plt.show()

#Defining the High pass Filter
def highpass(R1,R3,C1,C2,G,Vi):
    #s is the complex variable used
    s=symbols('s')
    #Defining A and b matrices obtained from circuit analysis
    A=Matrix([[0,0,1,-1/G],[-1/(1+1/(s*R3*C2)),1,0,0],[0,-G,G,1],[-s*C1-s*C2-1/R1,s*C2,0,1/R1]])
    b=Matrix([0,0,0,-Vi*s*C1])
    #Obtainig the Voltage matrix using A and b
    V = A.inv()*b
    return (A,b,V)
    
#Magnitude response of High Pass Filter
#Obatining A,b,V using the function defined
A,b,V = highpass(10000,10000,1e-9,1e-9,1.586,1)
#The fourth element of V matrix is the output voltage
Vo = V[3] 
#Converting the sympy Transfer function to Scipy LTI
H = converter(Vo)
#Defining w in log scale
w=np.logspace(0,8,801)
ss=1j*w
#Converting sympy function to numpy function
hf=lambdify(s,Vo,'numpy')
v=hf(ss)
#Plotting the Magnitude Response of High Pass Filter
plt.figure(2)
#Plotting in log scale
plt.loglog(w,abs(v),lw=2)
plt.xlabel(r'$w\rightarrow$')
plt.ylabel(r'$|H(jw)|\rightarrow$')
plt.title("Magnitude response of High Pass Filter")
plt.grid(True)
plt.show()

#Response for damped sinusoids
t = np.linspace(0,10,1000)
#Defining the input as low frequency Damped sinusoid
Vi = np.multiply(np.multiply(np.exp(-0.2*t),np.sin(2*np.pi*2*t)),np.heaviside(t,0.5))
#Obtaining the output voltage
Vo = sp.lsim(H,Vi,T=t)
#Plotting the Input and Output Voltage
plt.figure(3)
plt.plot(Vo[0],Vi,label=r'$V_{i}$')
plt.plot(Vo[0],Vo[1],label='$V_{o}$')
plt.xlabel("$t$")
plt.ylabel("$V$")
plt.legend(loc ='upper right')
plt.title("Output for Low frequency Damped Sinusoid")
plt.grid(True)
plt.show()

t = np.linspace(0,0.0001,10000)
#Defining the input as High frequency Damped sinusoid
Vi = np.multiply(np.multiply(np.exp(-100*t),np.sin(2*np.pi*200000*t)),np.heaviside(t,0.5))
#Obtaining the output voltage
Vo = sp.lsim(H,Vi,T=t)
#Plotting the Input and Output Voltage
plt.figure(4)
plt.plot(Vo[0],Vi,label=r'$V_{i}$')
plt.plot(Vo[0],Vo[1],label='$V_{o}$')
plt.xlabel("$t$")
plt.ylabel("$V$")
plt.legend(loc ='upper right')
plt.title("Output for High frequency Damped Sinusoid")
plt.grid(True)
plt.show()

#Step response
t = np.linspace(0,0.001,10000)
#Obtaining the Step response for HPF
Vo = sp.step(H,None,T=t)
#Plotting the step response for HPF
plt.figure(5)
plt.plot(Vo[0],Vo[1])
plt.xlabel("$t$")
plt.ylabel("$V_{o}$")
plt.title("Step Response of High Pass Filter")
plt.grid(True)
plt.show()
