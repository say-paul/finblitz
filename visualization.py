import matplotlib.pyplot as plt 
import ast
def fname(a):
    path= "/home/jhilikkundu/finblitz/historical_data/intraday/" + a
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
            elif key== 'volume':
                vol.append(g[k][key])

    fig,ax= plt.subplots(2,figsize=(10,10))
    ax[0].plot(date,lpt)
    ax[1].plot(date,vol)

    print("date = {}".format(date))
    print("ltp values = {}".format(lpt))
    print("volume values = {}".format(vol))
    
a= str(input("enter the file name to visualize data : "))
fname(a)
