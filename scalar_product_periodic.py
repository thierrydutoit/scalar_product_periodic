import streamlit as st
from numpy import *
from matplotlib.pyplot import *
import matplotlib.patches as mpatches
from mpl_toolkits import mplot3d
import cmath as math

st.title('Scalar Product: <sine,phasor>')

col1, col2 = st.columns(2)
with col1:
   f0=st.slider('Frequency of the sine wave: f0 [Hz]', 0, 10, 1)
with col2:
   dur=st.slider('Duration [s]',1, 20, 4)
   f=st.slider('Frequency of the phasor: f [Hz]', -10.0, 10.0, 1.0)
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
   st.markdown('''The three plots on the top left show rectangle, triangle and sinc functions 
               which can be modified using sliders _a_ and $\Delta$ . Notice that the integral 
               of these functions is always 1, whatever _a_.''')
   st.markdown('''When _a_ tends to infinity, these functions can no longer be plotted. 
               They are therefore symbolically represented in the bottom plotas an arrow, the 
               amplitude of which is set to the integral of the function: 1, and termed as 
               a _dirac impluse_ $\delta(t)$, shown on the right.''')
   st.markdown('''In the next four plots, we multiply our three functions with _f(t)=2cos(3t)_. 
               Then we compute the integral of this product. The integral is the area in blue
               (taken with signs). Multiplying the Dirac impulse by _2cos(3t)_ simply changes
                the value of the impulse.''')
   st.markdown('''When _a_ grows, we see that our three functions, although not fully identical, 
               tend to have the same effect _when used in an integral_: only their values very 
               close to their maximum contribute to the result. As a matter of fact, when
               $\Delta$ is set to 0, all integrals tends to $f(0)$:''')
   st.latex('''\int_{-\infty}^{\infty} f(t) \ \delta(t) \,dt=f(0)''')
   st.markdown('''When $\Delta$ is modified, all integrals tend to $f(\Delta)$:''')
   st.latex('''\int_{-\infty}^{\infty} f(t) \ \delta(t-\Delta) \,dt=f(\Delta)''')
