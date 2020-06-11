
from queue import Queue
import ast
from tabulate import tabulate
from utils import cleanse
from threading import Thread
import pandas as pd
import time
from termcolor import colored, cprint
import sys
now = time.time()
bsv = "historical_data/buyer_seller_volume/"
intra = "historical_data/intraday/"
script_names = "data/stock"


def runner(ticker, threshold=51):
    try:
            with open(bsv+ticker, "r") as f:
                data = f.read()
            data_bsv = ast.literal_eval(data)

        #     with open(intra+ticker, "r") as f:
        #         data = f.read()
        #     f.close()
    except:
        return "999"
    # data_intra = ast.literal_eval(data)
    data_bsv = cleanse(data_bsv)
    # data_intra = cleanse(data_intra)
    delivery_ratio = sort_by_deliverable_parcent(data_bsv, "deliveryToTradedQuantity")
    if float(delivery_ratio) >= threshold:
        return  delivery_ratio
    return "999"

def threader(q,t):

    while True:
        ticker = q.get(timeout=12)
        out = float(runner(ticker))
        if out != 999:
            # print("{} : {} ".format(ticker,str(out)))
            t.append([ticker, out])
        q.task_done()

def sort_by_deliverable_parcent(data_ticker,params):
    try:
        last_row = list(data_ticker.items())[-1]
        return last_row[1][params]
    except Exception as e:
        print ("error while fetching {}".format(e))
        return "0"

def main(workers,threshold):
    value_list = {}
    t = []
    with open(script_names,"r") as f:
        data = f.read()
    t_list = data.split("\n")
    q = Queue(maxsize=0)
    cprint('\nStarting thread..', 'green',file=sys.stderr)
    for i in range(workers):
        worker = Thread(target=threader,args=(q,t))
        worker.setDaemon(True)
        worker.start()
    cprint('\nProcessing..!!', 'yellow', attrs=['blink'], file=sys.stderr)
    for ticker in t_list:
        q.put(ticker)
    q.join()
    df = pd.DataFrame(t,columns=['ticker','deliveryRate'])
    df.apply(pd.to_numeric, errors='ignore')
    df.sort_values(by=['deliveryRate'], inplace=True,ascending=False)
    # more options can be specified also
    # with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    #     print(df)
    print(tabulate(df, headers='keys', tablefmt='psql'),)
main(10,50)
print("time taken: {}".format(str(time.time()-now)))
cprint('\n--Done--', 'blue', attrs=['bold'])
