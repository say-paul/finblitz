import json
import os
def autoSave():
	global lsave
	curr_time = time.time()
	if(curr_time >= lsave + 300):
		with open('infy', 'a+') as f:
			f.write(str(data_infy))
		with open('tcs', 'a+') as f:
			f.write(str(data_tcs))
		lsave = time.time()
		# combiner()
		print("AutoSaved at : " + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(lsave)))


def combiner(filepath,file_names):
    
	for ticker in file_names:
		if os.path.exists(filepath+"/"+ticker):
			final = {}
			with open(filepath+"/"+ticker, 'r') as f:
				data = f.read()
			data = data.replace("}{","}split{")
			splittedData = data.split('split')
			
			for dictionary in splittedData:
				tmp = json.loads(dictionary.replace("'",'"'))
				for key in tmp.keys():
					final[key] = tmp[key]
		
			with open(filepath+"/"+ticker, 'w') as fw:
				fw.write(str(final))

def cleanse(ticker_data):
	try:
		for keys in ticker_data:
			for attr in ticker_data[keys]:
				if ticker_data[keys][attr] == "-":
					ticker_data[keys][attr] = "0"
				ticker_data[keys][attr] = ticker_data[keys][attr].replace(',', '')
	except Exception as e:
            print("{} : {}".format(attr, e))
	finally:
		return ticker_data
