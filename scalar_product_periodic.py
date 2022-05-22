import streamlit as st
from numpy import *
from matplotlib.pyplot import *
import matplotlib.patches as mpatches
from mpl_toolkits import mplot3d
import cmath as math

st.title('Scalar Product: <sine,phasor>')

col1, col2 = st.columns(2)
with col1:
   f0=st.slider('Frequency of the sine wave: f0 [Hz]', 0, 5, 1)
with col2:
   dur=st.slider('Duration [s]',1, 10, 4)
   f=st.slider('Frequency of the phasor: f [Hz]', -5, 5, 1.0)
with col1:
   time_stamp=st.slider('Time stamp [s]', 0.0, dur*1.0, 0.0)

fe=10000;
t=arange(0,dur,1/fe) 

def rect(x):
    return where(abs(x)<=0.5, 1, 0)

def tri(x):
    return where(abs(x)<=1,1-abs(x),0)

def sincard(x):
    return divide(sin(pi*x),(pi*x))

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

signal=cos(2*pi*f0*t)

fig1,ax1 = subplots(figsize=(10,3))
xlim(0,dur); 
plot(t,signal)
grid()
title('$x(t)$')
xlabel('Time [s])')   
ax1.plot(time_stamp,cos(2*pi*f0*time_stamp),'o')
st.pyplot(fig1)

#st.latex('<x(t)\ ,\ e^{\ j\ 2\pi\ f\ t}>=1/{dur}\int_{0}^{dur} x(t) \ e^{\ -j\ 2\pi\ f\ t \ dt}')
phasor_real=cos(-2*pi*t*f)
phasor_imag=sin(-2*pi*t*f)
prod_real=multiply(phasor_real,signal)
scal_prod_real=sum(prod_real)/fe/dur
prod_imag=multiply(phasor_imag,signal)
scal_prod_imag=sum(prod_imag)/fe/dur
scal_prod_abs,scal_prod_arg=math.polar(complex(scal_prod_real,scal_prod_imag))
time_stamp_real=cos(-2*pi*time_stamp*f)*cos(2*pi*f0*time_stamp)
time_stamp_imag=sin(-2*pi*time_stamp*f)*cos(2*pi*f0*time_stamp)
time_stamp_abs,time_stamp_arg=math.polar(complex(time_stamp_real,time_stamp_imag))

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
   ax.plot(time_stamp, time_stamp_real,time_stamp_imag,'o')
   ax.plot([0,dur],[scal_prod_real,scal_prod_real],[scal_prod_imag,scal_prod_imag])
   title(r'$x(t)\ e^{-\ j\ 2\pi\ f\ t}$')
   st.pyplot(fig)

with col2:
   fig,ax = subplots(figsize=(3,3),subplot_kw={'projection': 'polar'})
   ax.plot(-2*pi*t*f+(signal<0)*pi,abs(signal))
   title(r'$x(t)\ e^{-\ j\ 2\pi\ f\ t}$')
   ax.plot(time_stamp_arg,time_stamp_abs,'o')
   ax.plot(scal_prod_arg,scal_prod_abs,'o')
   convert_polar_xticks_to_radians(ax)
   st.pyplot(fig)

with st.expander("Open for comments"):
   st.markdown('''The first plot shows a periodic signal $x(t)$ with adjustable frequency $f_0$ and duration $D$.''')
   st.markdown('''The two bottom plots show the product between this signal and a phasor with adjustable 
               frequency $f$. The _time stamp_ slider shows a specific instant on all plots.
               The bottom left plot shows the product in the complex plane as a function of time.
               The bottom right plot shows a side view of the same product, in the complex plane.
               ''')
   st.markdown('''The scalar product is is shown in green. It is the center of gravity of the product signal:
               ''')
   st.latex('''<x(t),x(t)\ e^{-\j\ 2\pi\ f\ t} = 1/T_0 \int_{-\0}^{\T_0} x(t)\ \ e^{-\j\ 2\pi\ f\ t}\ dt''')
