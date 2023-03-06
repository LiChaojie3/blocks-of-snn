from msdsl import *
#set neuron parameter
dt1=0.25
Tm = 20
El = -2
V_threshold = 2
R = 100
I = 0.06

#set memristor parameter
dt2 =0.0001
a, b = -2000, -250000
ron, roff = 100, 10000
Vt = 2

m = MixedSignalModel('lif_tb_lif_sum')

#set clock and reset signal
m.add_digital_input('clk')
m.add_digital_input('rst')

#set lif_neuron_1 signal
v1 = m.add_analog_output('v1',init = -2)
v1_1 = m.add_analog_state('v1_1',range_ = 5,init = -2)
flag_1 = m.add_digital_state('flag_1',init=1,width=1,signed=False)

#set tb_memristor signal
r = m.add_analog_state('r', range_ = 10000,init = 5000)
i = m.add_analog_state('i',range_ = 0.04)
flag1 = m.add_digital_state('flag1',init=1,width=1,signed=False)
flag2 = m.add_digital_state('flag2',init=1,width=1,signed=False)
flag3 = m.add_digital_state('flag3',init=1,width=1,signed=False)
flag4 = m.add_digital_state('flag4',init=1,width=1,signed=False)

#set lif_neuron_2 signal
v2 = m.add_analog_output('v2',init = -1)
v2_1 = m.add_analog_state('v2_1',range_ = 5,init = -1)
flag_2 = m.add_digital_state('flag_2',init=1,width=1,signed=False)
flag_3 = m.add_digital_state('flag_3',init=1,width=1,signed=False)
v = m.add_analog_state('v',range_ = 4)

#lif_neuron_1 modeling equation
m.set_this_cycle(flag_1,v1<V_threshold)
m.set_next_cycle(v1, (v1 + dt1*(1/Tm)*((El - v1)+ R*I))*flag_1-2*(~flag_1),clk=m.clk, rst=m.rst)
m.set_next_cycle(v1_1, v1*flag_1+4*(~flag_1),clk=m.clk, rst=m.rst)

#tb_memristor modeling equation
m.set_this_cycle(v, v2 - v1)
m.set_this_cycle(flag1,v>-Vt)
m.set_this_cycle(flag2,v>Vt)
m.set_this_cycle(flag3,r>ron)
m.set_this_cycle(flag4,r<roff)

m.set_next_cycle(r, r+dt2*(b*v+0.5*(a-b)*((v+Vt)*flag1-(v+Vt)*(~flag1)-(v-Vt)*flag2+(v-Vt)*(~flag2))*flag3*flag4),clk=m.clk, rst=m.rst)
func = lambda r: 1/r
f = m.make_function(func,
    domain=[100, 10000], numel=1000, order=1)
g = m.set_from_sync_func('g', f, r,clk=m.clk, rst=m.rst)
m.set_this_cycle(i, g*v)

#lif_neuron_2 modeling equation
m.set_this_cycle(flag_2,v2<V_threshold)
m.set_this_cycle(flag_3,i>0)
m.set_next_cycle(v2, (v2 + dt1*(1/Tm)*((El - v2)+ R*I + 800*i*flag_3 - 800*i*(~flag_3)))*flag_2-2*(~flag_2),clk=m.clk, rst=m.rst)
m.set_next_cycle(v2_1, v2*flag_2+4*(~flag_2),clk=m.clk, rst=m.rst)

m.compile_to_file(VerilogGenerator())