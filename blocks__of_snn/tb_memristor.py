from msdsl import *
#set parameter
dt =0.00008
a, b = -2000, -190000
ron, roff = 100, 10000
Vt = 1

m = MixedSignalModel('tb_memristor')

#set clock and reset signal
m.add_digital_input('clk')
m.add_digital_input('rst')

#set input and output signals
v = m.add_analog_input('v')
r = m.add_analog_output('r', init = 10000)
i = m.add_analog_output('i')

flag1 = m.add_digital_state('flag1',init=1,width=1,signed=False)
flag2 = m.add_digital_state('flag2',init=1,width=1,signed=False)
flag3 = m.add_digital_state('flag3',init=1,width=1,signed=False)
flag4 = m.add_digital_state('flag4',init=1,width=1,signed=False)

m.set_this_cycle(flag1,v>-Vt)
m.set_this_cycle(flag2,v>Vt)
m.set_this_cycle(flag3,r>ron)
m.set_this_cycle(flag4,r<roff)

m.set_next_cycle(r, r+dt*(b*v+0.5*(a-b)*((v+Vt)*flag1-(v+Vt)*(~flag1)-(v-Vt)*flag2+(v-Vt)*(~flag2))*flag3*flag4),clk=m.clk, rst=m.rst)
func = lambda r: 1/r
f = m.make_function(func,
    domain=[100, 10000], numel=500, order=1)
g = m.set_from_sync_func('g', f, r,clk=m.clk, rst=m.rst)
m.set_this_cycle(i, g*v)
m.compile_to_file(VerilogGenerator())