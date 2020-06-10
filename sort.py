# def volumeSort(buy_price,sell_price,trade_volume_ratio):
from queue import Queue
import ast
from prettytable import PrettyTable
from utils import cleanse
bsv = "historical_data/buyer_seller_volume/"
intra = "historical_data/intraday/"
script_names = "data/stock"

q = Queue(maxsize=0)


def threader(q):
    while True:
        ticker = q.get(timeout=12)
        runner(ticker)
        q.task_done()

def sort_by_deliverable_parcent(data_ticker,params):
    try:
        last_row = list(data_ticker.items())[-1]
        return last_row[1][params]
    except Exception as e:
        print ("error while fetching {}".format(e))
        return "0"


def main(threshold):
    value_list = {}
    with open(script_names,"r") as f:
        data = f.read()
    t_list = data.split("\n")
    for ticker in t_list:
        try:    
            with open(bsv+ticker,"r") as f:
                data = f.read()
            data_bsv = ast.literal_eval(data)

        #     with open(intra+ticker, "r") as f:
        #         data = f.read()
        #     f.close()
        except:
            continue
        # data_intra = ast.literal_eval(data)
        data_bsv = cleanse(data_bsv)
        # data_intra = cleanse(data_intra)
        delivery_ratio = sort_by_deliverable_parcent(data_bsv, "deliveryToTradedQuantity")
        if float(delivery_ratio) >= threshold:
            value_list[ticker] = float(delivery_ratio)
    value_list = sorted(value_list.items(), key=lambda kv: (kv[1], kv[0]),reverse=True)
    t = PrettyTable(['ticker', '%delivery'])
    for i in value_list:
        t.add_row([i[0], i[1]])
    print(t)
main(50)
