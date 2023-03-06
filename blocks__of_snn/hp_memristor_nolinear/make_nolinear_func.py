import csv

def make_nolinear_func(M,func,csv_ini,input,output,order=0,rst=None,clk=None):
    look_up = []
    with open(csv_ini,'r',newline='') as csv_f:
        reader = csv.reader(csv_f)
        for row in reader:
            csv_row = []
            for data in row:
                csv_row.append(float(data))
            csv_row[-1]=int(csv_row[-1])
            look_up.append(csv_row)    
            
    print(look_up)
    numel = len(look_up)  #段数
    
    out_signals = []   #每段的输出
    func_express = 0
    for i in range(0,numel):            
        f = M.make_function(func,domain=[look_up[i][0], look_up[i][1]], numel=look_up[i][2], order=order,write_tables=True)
        # 每段对应一个表，输出是a_i
        out_signal_name = str(output)+f'_out_{i}'
        out_signal = M.set_from_sync_func(out_signal_name, f, input,clk=clk,rst=rst)
        out_signals.append(out_signal)
        if numel==1:
            func_express += out_signals[i]
        else:
            if i==0:
                func_express += (input<look_up[i][1])*out_signals[i]
            elif i==numel-1:
                func_express += (look_up[i][0]<=input)*out_signals[i]
            else:
                func_express += (look_up[i][0]<=input)*(input<look_up[i][1])*out_signals[i]
    
    M.set_this_cycle(output, func_express)
