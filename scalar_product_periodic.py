import streamlit as st
from numpy import *
from matplotlib.pyplot import *
import matplotlib.patches as mpatches
from mpl_toolkits import mplot3d
import cmath as math

def periodic_square(t,f0):
    return where(abs((t%(1/f0))*f0)<=0.5, 1, -1)

def periodic_sawtooth(t,f0):
    return 2*(1-abs((t%(1/f0))*f0))-1

def format_radians_label(float_in):
    # Converts a float value in radians into a
    # string representation of that float
    string_out = str(float_in / (np.pi))+"π"
    return string_out

def convert_polar_xticks_to_radians(ax):
    # Converts x-tick labels from degrees to radians
    # Get the x-tick positions (returns in radians)
    label_positions = ax.get_xticks()
    # Convert to a list since we want to change the type of the elements
    labels = list(label_positions)
    # Format each label (edit this function however you'd like)
    labels = [format_radians_label(label) for label in labels]
    ax.set_xticklabels(labels)

st.title('Measuring frequency content')

st.markdown('''Suppose you are given a black box with some unknown periodic signal $x_{T_0}(t)$ in it, 
               whose fundamental amplitude $a$, frequency $f_{0}=1/T_{0}$ and and initial phase $\phi$ 
               are unknown.
               Suppose the only thing you can do is to provide another signal $in(t)$ as input, in which 
               case the black box will output the inner product between the two: $<x_{T_0}(t),in(t)>$. ''')
st.markdown('''What kind of periodic signal should you use as input to get the frequency, amplitude 
               and phase of the fundamental frequency component of $x_{T_0}(t)$? ''')
   

option = st.selectbox(
     'Choose a periodic signal', ('Cosine', 'Square', 'Sawtooth'))   

col1, col2, col3 = st.columns(3)
with col1:
   a=st.slider('Amplitude: a ', 0.5, 2.0, 1.0)
with col2:
   f0=st.slider('Frequency: f0 [Hz]', 1, 5, 1)*1.0
with col3:
   phi=st.slider('Initial phase: phi [rad]',-pi,pi,0.0)

fe=10000;
dur=2.0
time_stamp=st.slider('Time stamp [s]', 0.0, dur*1.0, 0.0)
sample_stamp=int(ceil(time_stamp*fe)-1)
t=arange(0,dur,1/fe) 

if option == 'Cosine' :
   signal=cos(2*pi*f0*t+phi)
elif option == 'Square' : 
    signal=periodic_square(t+(phi/2/np.pi/f0),f0)
else : signal=periodic_sawtooth(t+(phi/2/np.pi/f0),f0)

fig1,ax1 = subplots(figsize=(10,3))
xlim(0,dur); 
plot(t,signal)
grid()
title('$x_{T_0}(t)$')
xlabel('Time [s])')   
ax1.plot(time_stamp,signal[sample_stamp],'o')
st.pyplot(fig1)

st.markdown('''Let us choose a phasor as $e^{j2\pi ft}$ as input singal $in(t)$, and vary its frequency _f_''')
f =st.slider('Frequency of the phasor: f [Hz]', -5, 5, 1)

phasor_real=cos(-2*pi*t*f)
phasor_imag=sin(-2*pi*t*f)
prod_real=multiply(phasor_real,signal)
prod_imag=multiply(phasor_imag,signal)
scal_prod_real=sum(prod_real)/fe
scal_prod_imag=sum(prod_imag)/fe
scal_prod_abs,scal_prod_arg=math.polar(complex(scal_prod_real,scal_prod_imag))
prod_time_stamp_real=cos(-2*pi*time_stamp*f)*cos(2*pi*f0*time_stamp)
prod_time_stamp_imag=sin(-2*pi*time_stamp*f)*cos(2*pi*f0*time_stamp)

prod_time_stamp_real=prod_real[sample_stamp]
prod_time_stamp_imag=prod_imag[sample_stamp]

prod_time_stamp_abs,prod_time_stamp_arg=math.polar(complex(prod_time_stamp_real,prod_time_stamp_imag))

col1, col2 = st.columns(2)

with col1:
   fig,ax = subplots(figsize=(3,3),subplot_kw={'projection': '3d'})
   ax.plot3D(t, prod_real, prod_imag)
   #ax.plot3D(t, phasor_real, phasor_imag,'w--')
   ax.set_xlabel('Time [s])')
   ax.set_ylabel('real')
   ax.set_zlabel('imag')
   ax.set_ylim(-1,1)
   ax.set_zlim(-1,1)
   ax.plot(time_stamp, prod_time_stamp_real,prod_time_stamp_imag,'o')
   ax.plot([0,dur],[scal_prod_real/dur,scal_prod_real/dur],[scal_prod_imag/dur,scal_prod_imag/dur])
   title(r'$x_{T_0}(t)\ e^{-\ j\ 2\pi\ f\ t}$')
   st.pyplot(fig)

with col2:
   fig,ax = subplots(figsize=(3,3),subplot_kw={'projection': 'polar'})
   ax.plot(-2*pi*t*f+(signal<0)*pi,abs(signal))
   title(r'$x_{T_0}(t)\ e^{-\ j\ 2\pi\ f\ t}$')
   ax.plot(prod_time_stamp_arg, prod_time_stamp_abs,'o')
   ax.plot(scal_prod_arg,scal_prod_abs/dur,'o')
   convert_polar_xticks_to_radians(ax)
   st.pyplot(fig)

with st.expander("Open for comments"):
   st.markdown('''The first plot shows a periodic signal $x_{T_0}(t)$ with adjustable amplitude $a$, frequency $f_0$ 
                  and phase $phi$.''')
   st.markdown('''The two bottom plots show the product between this signal and a phasor with adjustable 
                  frequency $f$: \\
                  - the bottom left plot shows the product signal (in blue) as a function of time. \\
                  - the bottom right plot shows a side view of the same product signal, in the complex plane.
                  The circle with unity radius is the trace of the phasor. ''')
   st.markdown('''The _time stamp_ slider shows a specific instant on all plots, in orange.''')
   st.markdown('''If we assume that the curve has a uniform weight, its center of gravity (CG) is shown in green. 
                  It is intuivively the place where to support the curve so as to maintain its balance.   ''')
   st.markdown('''As we can see, the position of the CG of the product between phasor $e^{j2\pi ft}$ 
                  and our signal with frequency $f_0$ is non-zero only when $f=k \ f_0$ (with $k$ integer). 
                  Its modulus and argument for $k=1$ provide the solution to our problem: $a$ is twice the 
                  modulus of the CG and $phi$ is the argument of the CG. ''') 
   st.markdown('''If we now assume that each segment of duration $dt$ of the product curve has a mass $dt$ - so that the total 
                  mass of one period of this curve is precisely $T_0$ - then this center of gravity is nothing 
                  else than the inner product:''')
   st.latex('''<x_{T_0}(t),e^{j 2\pi f_0 t}> =\dfrac{\int_{0}^{T_0} x{T_0}(t)\ e^{-j2\pi f_0 t}\ dt}{T_0}''')
   st.markdown('''As a result, our black box will provide this CG as output, i.e., $a$, $f_0$, and $phi$.''')
   st.markdown('''Notice, finally, that when our periodic signal is a cosine, the only two non-zero inner products 
                  give us exactly the composition of our cosine in terms of phasors:''')
   st.latex('''a\cos(2\pi f_{0}t+\phi)=<x(t),e^{j2\pi f_0t}>e^{j2\pi f_0 t} + <x(t),e^{-j2\pi f_0 t}>\ e^{-j2\pi f_0 t}''')
   st.latex('''=\dfrac{a}{2} e^{j\phi} e^{j2\pi f_0 t} + \dfrac{a}{2} e^{-j\phi} e^{-j2\pi f_0 t}''')
   st.markdown('''This can be generalized the inner product of a periodic signal with phasors provides thte frequency content of the signal.''')

