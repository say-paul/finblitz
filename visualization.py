import matplotlib.pyplot as plt 
import ast
def fname(a):
    path= "/home/jhilikkundu/finblitz/historical_data/intraday/" + a
    path2="/home/jhilikkundu/finblitz/historical_data/buyer_seller_volume/" + a
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
    fig.autofmt_xdate(rotation=90)
    plt.grid(b='on')
    plt.gca().invert_yaxis()
    plt.savefig('rvnl.png')
    #print("date = {}".format(date))
    #print("ltp values = {}".format(lpt))
    #print("volume values = {}".format(vol))
    
a= str(input("enter the file name to visualize data : "))
fname(a)
