from msdsl import *
import numpy as np
from math import exp
#set neuron parameter
dt1=0.25
Tm = 20
El = -2
V_threshold = 2
R = 100
I = 0.06

#set memristor parameter
dt2 = 4e-6
Xp, Xn = 0.9, 0.1
ap, an, Ap, An = 0.1, 0.4, 150, 300
a1, a2, h = 0.00006, 0.00006, 2.1
Vp, Vn = 2, 2
DOMAIN = 4

m = MixedSignalModel('lif_eg_lif_sum')

#set clock and reset signal
m.add_digital_input('clk')
m.add_digital_input('rst')

#set lif_neuron_1 signal
v1 = m.add_analog_output('v1',init = -2)
v1_1 = m.add_analog_state('v1_1',range_ = 5,init = -2)
flag_1 = m.add_digital_state('flag_1',init=1,width=1,signed=False)

#set eg_memristor signal 
x = m.add_analog_output('x', init = 0.3)
i = m.add_analog_state('i',range_ = 0.2, init = 0)

flag1 = m.add_digital_state('flag1',init=1,width=1,signed=False)
flag2 = m.add_digital_state('flag2',init=1,width=1,signed=False)
flag3 = m.add_digital_state('flag3',init=1,width=1,signed=False)
flag4 = m.add_digital_state('flag4',init=1,width=1,signed=False)
flag5 = m.add_digital_state('flag5',init=1,width=1,signed=False)

#set lif_neuron_2 signal
v2 = m.add_analog_output('v2',init = 0.41)
v2_1 = m.add_analog_state('v2_1',range_ = 5,init = 0.41)
flag_2 = m.add_digital_state('flag_2',init=1,width=1,signed=False)
flag_3 = m.add_digital_state('flag_3',init=1,width=1,signed=False)
v = m.add_analog_output('v')

#lif_neuron_1 modeling equation
m.set_this_cycle(flag_1,v1<V_threshold)
m.set_next_cycle(v1, (v1 + dt1*(1/Tm)*((El - v1)+ R*I))*flag_1-2*(~flag_1),clk=m.clk, rst=m.rst)
m.set_next_cycle(v1_1, v1*flag_1+4*(~flag_1),clk=m.clk, rst=m.rst)

#eg_memristor modeling equation
m.set_this_cycle(v, v2 - v1)
m.set_this_cycle(flag1,v<0)
m.set_this_cycle(flag2,v<-Vn)
m.set_this_cycle(flag3,v>Vp)
m.set_this_cycle(flag4,x<Xp)
m.set_this_cycle(flag5,x>1-Xn)
eap=exp(ap*Xp)
ean=exp(an*(Xn-1))
evp=exp(Vp)
evn=exp(Vn)
func1 = lambda v:np.exp(v) 
f1 = m.make_function(func1, 
    domain=[-DOMAIN, DOMAIN], numel=100, order=1)
ev1 = m.set_from_sync_func('ev1', f1, v, clk=m.clk, rst=m.rst)

func2 = lambda v:1/np.exp(v) 
f2 = m.make_function(func2,
    domain=[-DOMAIN, DOMAIN], numel=100, order=1)
ev2 = m.set_from_sync_func('ev2', f2, v, clk=m.clk, rst=m.rst)

func3 = lambda v:np.exp(2.1*v) 
f3 = m.make_function(func3,
    domain=[-DOMAIN, DOMAIN], numel=100, order=1)
ev3 = m.set_from_sync_func('ev3', f3, v, clk=m.clk, rst=m.rst)

func4 = lambda v:1/np.exp(2.1*v) 
f4 = m.make_function(func4,
    domain=[-DOMAIN, DOMAIN], numel=100, order=1)
ev4 = m.set_from_sync_func('ev4', f4, v, clk=m.clk, rst=m.rst)

func5 = lambda x:np.exp(0.3*x) 
f5 = m.make_function(func5,
    domain=[0, 1], numel=40, order=1)
ex1 = m.set_from_sync_func('ex1', f5, x, clk=m.clk, rst=m.rst)

func6 = lambda x:1/np.exp(0.1*x) 
f6 = m.make_function(func6,
    domain=[0, 1], numel=40, order=1)
ex2 = m.set_from_sync_func('ex2', f6, x, clk=m.clk, rst=m.rst)

m.set_this_cycle(i, (a1*x*0.5*(ev3-ev4))*(~flag1)+(a2*x*0.5*(ev3-ev4))*flag1)
m.set_next_cycle(x, x+dt2*((Ap*(ev1-evp)*(flag3)+(-An)*(ev2-evn)*(flag2))*(ex2*eap*((Xp-x)/(1-Xp)+1)*(~flag1)*(~flag4)+ 1*(~flag1)*(flag4)+ex1*ean*(x/(1-Xn))*(flag1)*(~flag5)+1*(flag1)*(flag5))),clk=m.clk, rst=m.rst)

#lif_neuron_2 modeling equation
m.set_this_cycle(flag_2,v2<V_threshold)
m.set_this_cycle(flag_3,i>0)

m.set_next_cycle(v2, (v2 + dt1*(1/Tm)*((El - v2)+ R*(I + i*flag_3 - 1.50*i*(~flag_3))))*flag_2-2*(~flag_2),clk=m.clk, rst=m.rst)
m.set_next_cycle(v2_1, v2*flag_2+4*(~flag_2),clk=m.clk, rst=m.rst)

m.compile_to_file(VerilogGenerator())