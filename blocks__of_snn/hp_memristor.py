from msdsl import *
import numpy as np
#set parameter
dt=1e-3
k = 10000
ron, roff =100, 10000

m = MixedSignalModel('hp_memristor')

#set clock and reset signal
m.add_digital_input('clk')
m.add_digital_input('rst')

#set input and output signals
v = m.add_analog_input('v')
x = m.add_analog_output('x',init = 0.2)
i = m.add_analog_output('i')
r = m.add_analog_output('r')

m.set_next_cycle(x, x+k*dt*i,clk=m.clk, rst=m.rst)
m.set_this_cycle(r,x*ron+(1-x)*roff)
func = lambda r: 1/r
f = m.make_function(func,
    domain=[500, 9500], numel=450, order=1)
g = m.set_from_sync_func('g', f, r,clk=m.clk, rst=m.rst)
m.set_this_cycle(i,g*v)
m.compile_to_file(VerilogGenerator())