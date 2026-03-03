import json
import pandas as pd

PATH = "data/data_garage.json"
id = []
gateway = []
sensor = []
rssi = []
snr = []


with open(PATH, 'r') as file:
    raw_data = json.load(file)

for i in range(len(raw_data) - 1):
    if (raw_data[i]["name"] == "as.up.data.forward"):
        for j in range(len(raw_data[i]["data"]["uplink_message"]["rx_metadata"])):
            id.append(raw_data[i]["data"]["uplink_message"]["f_cnt"])
            sensor.append(raw_data[i]["data"]["end_device_ids"]["device_id"])
            gateway.append(raw_data[i]["data"]["uplink_message"]["rx_metadata"][j]["gateway_ids"]["gateway_id"])
            rssi.append(raw_data[i]["data"]["uplink_message"]["rx_metadata"][j]["rssi"])
            snr.append(raw_data[i]["data"]["uplink_message"]["rx_metadata"][j]["snr"])

DATA = pd.DataFrame({'GATEWAY': gateway,
                    'RSSI': rssi,
                    'SNR': snr},
                    index=[id, sensor])

print(DATA)