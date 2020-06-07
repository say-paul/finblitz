import urllib.request
import json
import time
import os
from queue import Queue
from threading import Thread
from utils import combiner

def import_web(ticker):
    """
    :param ticker: Takes the company ticker
    :return: Returns the HTML of the page
    """
    url = 'https://www.nseindia.com/live_market/dynaContent/live_watch/get_quote/GetQuote.jsp?symbol='+ticker+'&illiquid=0&smeFlag=0&itpFlag=0'
    req = urllib.request.Request(url, headers={'User-Agent' : "PostmanRuntime/7.25.0"}) 
    fp = urllib.request.urlopen(req, timeout=10)
    mybytes = fp.read()
    mystr = mybytes.decode("utf8")
    fp.close()
    return mystr


def get_quote(ticker):
    """
    :param ticker: Takes the company ticker
    :return: None
    """
    ticker = ticker.upper()
    try:
        print("fetching data for {}".format(ticker))
        string_html = filter_data(import_web(ticker))
        # exit()
        # get_data(string_html,ticker)
    except Exception as e:
        print("{} for {}".format(e,ticker))
        retry_list.append(ticker)

    return string_html

          
def filter_data(string_html):          
    searchString = '<div id="responseDiv" style="display:none">'
    #assign: stores html tag to find where data starts
    searchString2 = '</div>'
    #stores:  stores html tag where  data end
    sta = string_html.find(searchString)
    # returns & store: find() method returns the lowest index of the substring (if found). If not found, it returns -1.
    data = string_html[sta + 43:]
    #returns & stores: skips 43 characters and stores the index of substring
    end = data.find(searchString2)
    # returns & store: find() method returns the lowest index of the substring (if found). If not found, it returns -1.
    fdata = data[:end]
    #fetch: stores the fetched data into fdata
    stripped = fdata.strip()
    #removes: blank spaces
    return stripped


def intraday_price_data(stripped):
    js = json.loads(stripped)
    datajs = js['data'][0]
    subdictionary = {}
    subdictionary['ltp'] = datajs['lastPrice']
    subdictionary['open'] = datajs['open']
    subdictionary['high'] = datajs['dayHigh']
    subdictionary['low'] = datajs['dayLow']
    subdictionary['close'] = datajs['lastPrice']
    subdictionary['volume'] = datajs['totalTradedVolume']
    return {js['lastUpdateTime']: subdictionary}

         
def buyer_seller(stripped):
    js = json.loads(stripped)
    datajs = js['data'][0]
    subdictionary = {}
    for keys in datajs:
        if (keys.__contains__("buyPrice") or keys.__contains__("sellPrice") or
         keys.__contains__("buyQuantity") or keys.__contains__("sellQuantity")):
            subdictionary[keys] = datajs[keys]
    
    return {js['lastUpdateTime'] : subdictionary}

def runner(ticker):
    try:
        print("Starting get_quote for ", ticker)
        filtered_data = get_quote(ticker)
        volume_data = buyer_seller(filtered_data)
        with open(volume_path+"/"+ticker, 'a+') as f:
            f.write(str(volume_data))
        price_intraday = intraday_price_data(filtered_data)
        with open(intraday_path+"/"+ticker, 'a+') as f:
            f.write(str(price_intraday))

    except Exception as e:
        print(e)

def do_stuff(q):
    while True:
        ticker =  q.get()
        print("Ticker {}".format(ticker))
        runner(ticker)
        q.task_done()

def main():
    if not os.path.exists('historical_data'):
        os.makedirs('historical_data')
        os.makedirs('historical_data/buyer_seller_volume')
        os.makedirs('historical_data/intraday')
    with open(script_names,"r") as f:
        data = f.read()
    t_list = data.split("\n")
    for i in range(workers):
        worker = Thread(target=do_stuff, args=(q,))
        worker.setDaemon(True)
        worker.start()
    for ticker in t_list:
        q.put(ticker)
    q.join()
    
    for x in range(1):
        if (0 < len(retry_list)):
            print("error found {}....".format(str(len(retry_list))))
            print("retrying {} times....".format(x))
            for i in range(workers):
                worker = Thread(target=do_stuff, args=(q,))
                worker.setDaemon(True)
                worker.start()
            for ticker in retry_list:
                q.put(ticker)
            q.join()
    combiner(volume_path, t_list)
    combiner(intraday_path, t_list)


q = Queue(maxsize=0)
workers = 100
script_names = "data/test"
volume_path = "historical_data/buyer_seller_volume"
intraday_path = "historical_data/intraday"
retry_list = []
current = time.time()
main()
print("Time taken: {} sec".format(str(time.time()-current)))
