from msdsl import *
import numpy as np
from make_nolinear_func import *
#set parameter
dt=1e-3
k = 10000
ron, roff =100, 10000

m = MixedSignalModel('hp_memresistor')

#set clock and reset signal
m.add_digital_input('clk')
m.add_digital_input('rst')

#set input and output signals
v = m.add_analog_input('v')
x = m.add_analog_output('x',init = 0.2)
i = m.add_analog_output('i')
r = m.add_analog_output('r')

lut_file="/home/xiaotu/Desktop/msdsl-0.3.8/reciprocal_of_r.csv"
m.set_next_cycle(x, x+k*dt*i,clk=m.clk, rst=m.rst)
m.set_this_cycle(r,x*ron+(1-x)*roff)
func = lambda r: 1/r
make_nolinear_func(m,func,lut_file,r,'g',clk=m.clk,rst=m.rst)
m.set_this_cycle(m.i,m.g*m.v)
m.compile_to_file(VerilogGenerator())