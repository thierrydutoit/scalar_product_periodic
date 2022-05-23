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

st.title('<periodic signal, phasor>')

st.markdown('''Let us examine how the scalar product between a phasor $e^{-\j2\pi\f\t}$ with frequency _f_ 
               and _N_ periods of a periodic signal _x(t)_ of frequency _f0_ is obtained. ''')
   
col1, col2 = st.columns(2)
with col1:
   f0=st.slider('Frequency of the periodic signal: f0 [Hz]', 1, 5, 1)*1.0
   f =st.slider('Frequency of the phasor: f [Hz]', -5, 5, 1)
with col2:
   N_periods=st.slider('Number of periods: N',1, 10, 4)
   dur=N_periods/f0
   time_stamp=st.slider('Time stamp [s]', 0.0, dur*1.0, 0.0)

option = st.selectbox(
     'Choose a periodic signal', ('Cosine', 'Square', 'Sawtooth'))   

fe=10000;
t=arange(0,dur,1/fe) 

if option == 'Cosine' :
   signal=cos(2*pi*f0*t)
elif option == 'Square' : 
    signal=periodic_square(t,f0)
else : signal=periodic_sawtooth(t,f0)

fig1,ax1 = subplots(figsize=(10,3))
xlim(0,dur); 
plot(t,signal)
grid()
title('$x(t)$')
xlabel('Time [s])')   
ax1.plot(time_stamp,cos(2*pi*f0*time_stamp),'o')
st.pyplot(fig1)

phasor_real=cos(-2*pi*t*f)
phasor_imag=sin(-2*pi*t*f)
prod_real=multiply(phasor_real,signal)
prod_imag=multiply(phasor_imag,signal)
scal_prod_real=sum(prod_real)/fe
scal_prod_imag=sum(prod_imag)/fe
scal_prod_abs,scal_prod_arg=math.polar(complex(scal_prod_real,scal_prod_imag))
prod_time_stamp_real=cos(-2*pi*time_stamp*f)*cos(2*pi*f0*time_stamp)
prod_time_stamp_imag=sin(-2*pi*time_stamp*f)*cos(2*pi*f0*time_stamp)
prod_time_stamp_abs,prod_time_stamp_arg=math.polar(complex(prod_time_stamp_real,prod_time_stamp_imag))
phasor_time_stamp_real=cos(-2*pi*time_stamp*f)
phasor_time_stamp_imag=sin(-2*pi*time_stamp*f)
phasor_time_stamp_abs,phasor_time_stamp_arg=math.polar(complex(phasor_time_stamp_real,phasor_time_stamp_imag))

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
   title(r'$x(t)\ e^{-\ j\ 2\pi\ f\ t}$')
   st.pyplot(fig)

with col2:
   fig,ax = subplots(figsize=(3,3),subplot_kw={'projection': 'polar'})
   ax.plot(-2*pi*t*f+(signal<0)*pi,abs(signal))
   title(r'$x(t)\ e^{-\ j\ 2\pi\ f\ t}$')
   ax.plot([prod_time_stamp_arg, phasor_time_stamp_arg], [prod_time_stamp_abs, phasor_time_stamp_abs],'o')
   ax.plot(scal_prod_arg,scal_prod_abs/dur,'o')
   convert_polar_xticks_to_radians(ax)
   st.pyplot(fig)

with st.expander("Open for comments"):
   st.markdown('''The first plot shows a periodic signal $x(t)$ with adjustable frequency $f_0$ and duration $D$.''')
   st.markdown('''The two bottom plots show the product between this signal and a phasor with adjustable 
                  frequency $f$. 
                  The bottom left plot shows the product signal in the complex plane as a function of time.
                  The bottom right plot shows a side view of the same product signal, in the complex plane.
                  The circle with unity radius is the trace of the phasor. The shape in blue is the trace of 
                  the product signal.
               ''')
   st.markdown('''The _time stamp_ slider shows a specific instant on all plots, in orange.''')
   st.markdown('''The scalar product, computed on ONE period only, is is shown in green. 
                  It is the center of gravity of the product signal:''')
   st.latex('''<x(t),e^{-j\ 2\pi\ f\ t}> = 1/T_0 \int_{0}^{T_0} x(t)\ \ e^{-j\ 2\pi\ f\ t}\ dt''')
   st.markdown('''When computed on the number _N_ of periods shown on the top plot, the scalar product is 
                  multiplied by _N_. This is NOT shown on the plot.
                  ''')
