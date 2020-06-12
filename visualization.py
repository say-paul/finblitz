import matplotlib.pyplot as plt 
from matplotlib.ticker import (AutoMinorLocator, MultipleLocator)
import numpy as np
import matplotlib.ticker as ticker

import ast
def fname(a):
    path= "historical_data/intraday/" + a
    path2="historical_data/buyer_seller_volume/" + a
    with open (path2,"r") as f2:
        data2= f2.read()
        g2= ast.literal_eval(data2)
        f2.close()
    with open(path,"r") as f:
        data =f.read()
        g= ast.literal_eval(data)
        f.close()

    date=[]
    lpt=[]
    vol=[]
    for key in g:
        date.append(key)
        k=key
        for key in g[k]:
            if key== "ltp":
                lpt.append(g[k][key])
        for key in g2[k]:
            if key== 'deliveryToTradedQuantity':
                vol.append(g2[k][key])
    
    fig,axs= plt.subplots(2 ,figsize=(50,10))
    axs[0].plot(date,vol)
    axs[1].plot(date,lpt)
    
    for i in range(len(axs)):
    # Change major ticks to show every 20.
        axs[i].xaxis.set_major_locator(MultipleLocator(5))
        if (i != 0):
            axs[i].yaxis.set_major_locator(MultipleLocator(5))
        # Change minor ticks to show every 5. (20/4 = 5)
        axs[i].xaxis.set_minor_locator(AutoMinorLocator(4))
        axs[i].yaxis.set_minor_locator(AutoMinorLocator(4))
        # if (i != 0):
        #     axs[i].autoscale()
    axs[0].yaxis.set_ticks(np.arange(0, 100, 10))
    fig.autofmt_xdate(rotation=90)
    plt.grid(b=True)
    plt.gca().invert_yaxis()
    plt.savefig('rvnl.png')
    # plt.show()
    #print("date = {}".format(date))
    #print("ltp values = {}".format(lpt))
    #print("volume values = {}".format(vol))
    
a= str(input("enter the file name to visualize data : "))
fname(a)
