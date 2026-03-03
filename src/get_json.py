import json
import pandas as pd

PATH = "data/data_garage.json"

data_id = []
data_gateway = []
data_rssi = []
data_snr = []
sensor_id = []
sensor_sensor = []
temp_sensor_airtime = []
sensor_bw = []
sensor_sf = []

with open(PATH, 'r') as file:
    raw_data = json.load(file)

for i in range(len(raw_data) - 1):
    if (raw_data[i]["name"] == "as.up.data.forward"):
        sensor_id.append(raw_data[i]["data"]["uplink_message"]["f_cnt"])
        sensor_sensor.append(raw_data[i]["data"]["end_device_ids"]["device_id"])
        temp_sensor_airtime.append(raw_data[i]["data"]["uplink_message"]["consumed_airtime"])
        sensor_bw.append(raw_data[i]["data"]["uplink_message"]["settings"]["data_rate"]["lora"]["bandwidth"])
        sensor_sf.append(raw_data[i]["data"]["uplink_message"]["settings"]["data_rate"]["lora"]["spreading_factor"])
        for j in range(len(raw_data[i]["data"]["uplink_message"]["rx_metadata"])):
            data_id.append(raw_data[i]["data"]["uplink_message"]["f_cnt"])
            data_gateway.append(raw_data[i]["data"]["uplink_message"]["rx_metadata"][j]["gateway_ids"]["gateway_id"])
            data_rssi.append(raw_data[i]["data"]["uplink_message"]["rx_metadata"][j]["rssi"])
            data_snr.append(raw_data[i]["data"]["uplink_message"]["rx_metadata"][j]["snr"])
sensor_airtime = [float(t.replace('s', '')) for t in temp_sensor_airtime]

SENSOR = pd.DataFrame({'SENSOR': sensor_sensor,
                       'AIRTIME': sensor_airtime,
                       'BW': sensor_bw,
                       'SP': sensor_sf},
                       index=[sensor_id])


DATA = pd.DataFrame({'RSSI': data_rssi,
                    'SNR': data_snr},
                    index=[data_id, data_gateway])

print(DATA)
print(SENSOR)