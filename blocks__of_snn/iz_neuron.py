from msdsl import *
#set neuron parameter
dt1=1/64
a=0.02
b = 0.25
c = -65
d = 0.05
I = 15
p = 30

m = MixedSignalModel('iz_neurons')

#set clock and reset signal
m.add_digital_input('clk')
m.add_digital_input('rst')

#set output signal
v1 = m.add_analog_output('v1',init = -65)
u1 = m.add_analog_output('u1',init = -13)
flag_1 = m.add_digital_state('flag_1',init=1,width=1,signed=False)

m.set_this_cycle(flag_1,v1<p)
m.set_next_cycle(v1, (v1+dt1*(0.04*v1*v1+5*v1+140-u1+I))*flag_1 + c*(~flag_1),clk=m.clk, rst=m.rst)
m.set_next_cycle(u1, (u1+dt1*a*(b*v1-u1))*flag_1 + (u1+d)*(~flag_1),clk=m.clk, rst=m.rst)
m.compile_and_print(VerilogGenerator())