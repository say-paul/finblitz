# def volumeSort(buy_price,sell_price,trade_volume_ratio):
import ast
from tabulate import tabulate

bsv = "historical_data/buyer_seller_volume/"
intra = "historical_data/intraday/"
ticker = "CAREERP"
final_report = []
with open(bsv+ticker,"r") as f:
    data = f.read()
data_bsv = ast.literal_eval(data)

with open(intra+ticker, "r") as f:
    data = f.read()
    f.close()
data_intra = ast.literal_eval(data)
try:
    for keys in data_intra:
        buy_above_ltp, buy_below_ltp,sell_above_ltp,sell_below_ltp =0,0,0,0"
        try:
            data_bsv[keys]['deliveryToTradedQuantity']
        except:
            data_bsv[keys]['deliveryToTradedQuantity'] = "0"
        try:
            for attr in data_bsv[keys]:
                if data_bsv[keys][attr] == "-":
                    data_bsv[keys][attr] = "0"
                data_bsv[keys][attr] = data_bsv[keys][attr].replace(',', '')
                    
            for attr in data_intra[keys]:
                if data_intra[keys][attr] == "-":
                    data_intra[keys][attr] = "0"
                data_intra[keys][attr] = data_intra[keys][attr].replace(',', '')
        except Exception as e:
            print("{} : {}".format(attr, e))
        for m in range(5):
            if float(data_intra[keys]['ltp']) <= float(data_bsv[keys]['buyPrice' + str(m+1)]):
                buy_above_ltp += int(data_bsv[keys]['buyQuantity' + str(m+1)])
            else:
                buy_below_ltp += int(data_bsv[keys]['buyQuantity' + str(m+1)])
        
            if float(data_intra[keys]['ltp']) <= float(data_bsv[keys]['sellPrice' + str(m+1)]):
                sell_above_ltp += int(data_bsv[keys]['sellQuantity' + str(m+1)])
            else:
                sell_below_ltp += int(data_bsv[keys]['sellQuantity' + str(m+1)])
        buy_pressure = (buy_above_ltp-buy_below_ltp)/(buy_above_ltp+buy_below_ltp)
        sell_pressure = (sell_above_ltp-sell_below_ltp) / (sell_above_ltp+sell_below_ltp)
        final_report.append(
            [keys, data_intra[keys]['ltp'], data_intra[keys]['pChange'], data_bsv[keys]['deliveryToTradedQuantity'], buy_pressure, sell_pressure])
finally:
    print("************************************************************************".format(ticker))
    print("-------------------- {} : NSE INTRADAY TREND ---------------------".format(ticker))
    print("************************************************************************".format(ticker))
    print(tabulate(final_report, headers=[
          "   Date       Time", "LTP", "%change", "delivery%", "buyP", "sellP"]))


# -1(willing to sell at lower price, position book) < sellP < 1(want to bet better price)
# -1(willing to buy at low price) < buyP < 1(willing to buy at high price)