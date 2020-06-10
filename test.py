from utils import combiner

script_names = "data/stock"
volume_path = "historical_data/buyer_seller_volume"
intraday_path = "historical_data/intraday"
with open(script_names, "r") as f:
        data = f.read()
t_list = data.split("\n")

combiner(volume_path, t_list)
combiner(intraday_path,t_list)