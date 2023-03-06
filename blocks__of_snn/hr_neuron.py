from msdsl import *
#set neuron parameter
dt= 0.05
a = 1.0
b = 3.0
c = 1.0
d = 5.0
Urst = -1.6
s = 4
I = 1

m = MixedSignalModel('hr_neurons')

#set clock and reset signal
m.add_digital_input('clk')
m.add_digital_input('rst')

#set output signal
v = m.add_analog_output('v',init = -1.116)
u = m.add_analog_output('u',init = -6.03)
w = m.add_analog_state('w',range_ = 1.0,init = 0.049)

m.set_next_cycle(v, v+dt*(u-(a*v-b)*v*v+I-w), clk=m.clk, rst=m.rst)
m.set_next_cycle(u, u+dt*(c-d*v*v-u),clk=m.clk, rst=m.rst)
m.set_next_cycle(w, w+dt*(0.001*(s*(v-Urst)-w)), clk=m.clk, rst=m.rst)
m.compile_and_print(VerilogGenerator())