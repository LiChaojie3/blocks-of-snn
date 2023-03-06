from msdsl import *
import numpy as np
from math import exp
#set parameter
dt =  0.000012
Xp, Xn = 0.3, 0.5
ap, an, Ap, An = 1, 5, 4000, 4000
a1, a2, b = 0.17, 0.17, 0.05
Vp, Vn = 0.16, 0.15
DOMAIN = 1

m = MixedSignalModel('eg_memristor')

#set clock and reset signal
m.add_digital_input('clk')
m.add_digital_input('rst')

#set input and output signals
v = m.add_analog_input('v')
x = m.add_analog_output('x', init = 0.11)
i = m.add_analog_output('i')

flag1 = m.add_digital_state('flag1',init=1,width=1,signed=False)
flag2 = m.add_digital_state('flag2',init=1,width=1,signed=False)
flag3 = m.add_digital_state('flag3',init=1,width=1,signed=False)
flag4 = m.add_digital_state('flag4',init=1,width=1,signed=False)
flag5 = m.add_digital_state('flag5',init=1,width=1,signed=False)

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
    domain=[-DOMAIN, DOMAIN], numel=200, order=1)
ev1 = m.set_from_sync_func('ev1', f1, v, clk=m.clk, rst=m.rst)

func2 = lambda v:1/np.exp(v) 
f2 = m.make_function(func2,
    domain=[-DOMAIN, DOMAIN], numel=200, order=1)
ev2 = m.set_from_sync_func('ev2', f2, v, clk=m.clk, rst=m.rst)

func3 = lambda v:np.exp(0.05*v) 
f3 = m.make_function(func3,
    domain=[-DOMAIN, DOMAIN], numel=200, order=1)
ev3 = m.set_from_sync_func('ev3', f3, v, clk=m.clk, rst=m.rst)

func4 = lambda v:1/np.exp(0.05*v) 
f4 = m.make_function(func4,
    domain=[-DOMAIN, DOMAIN], numel=200, order=1)
ev4 = m.set_from_sync_func('ev4', f4, v, clk=m.clk, rst=m.rst)

func5 = lambda x:np.exp(x) 
f5 = m.make_function(func5,
    domain=[0, 1], numel=50, order=1)
ex1 = m.set_from_sync_func('ex1', f5, x, clk=m.clk, rst=m.rst)

func6 = lambda x:1/np.exp(x) 
f6 = m.make_function(func6,
    domain=[0, 1], numel=50, order=1)
ex2 = m.set_from_sync_func('ex2', f6, x, clk=m.clk, rst=m.rst)

m.set_this_cycle(i, (a1*x*0.5*(ev3-ev4))*(~flag1)+(a2*x*0.5*(ev3-ev4))*flag1)

m.set_next_cycle(x, x+dt*((Ap*(ev1-evp)*(flag3)+(-An)*(ev2-evn)*(flag2))*(ex2*eap*((Xp-x)/(1-Xp)+1)*(~flag1)*(~flag4)+ 1*(~flag1)*(flag4)+(ex1*ex1*ex1*ex1*ex1)*ean*(x/(1-Xn))*(flag1)*(~flag5)+1*(flag1)*(flag5))),clk=m.clk, rst=m.rst)
m.compile_to_file(VerilogGenerator())