from msdsl import *
#set neuron parameter
dt=0.25
Tm = 20
El = -2
V_threshold = 2
R = 100
I = 0.06

m = MixedSignalModel('lif_neurons')

#set clock and reset signal
m.add_digital_input('clk')
m.add_digital_input('rst')

#set output signal
v = m.add_analog_output('v',init = -2)
flag = m.add_digital_state('flag',init=1,width=1,signed=False)

m.set_this_cycle(flag,v<V_threshold)
m.set_next_cycle(v, (v + dt*(1/Tm)*((El - v)+ R*I))*flag-2*(~flag),clk=m.clk, rst=m.rst)
m.compile_and_print(VerilogGenerator())