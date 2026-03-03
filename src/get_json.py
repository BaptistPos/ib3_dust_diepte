import json
import pandas as pd

AG2AG_PATH = "data/data_garage.json"
UG2AG_PATH = "data/data_huis_midden.json"

def get_json(path):
    s_id, s_cnt, s_sensor, s_airtime, s_bw, s_sf = [], [], [], [], [], []
    d_id, d_cnt, d_gateway, d_rssi, d_snr = [], [], [], [], []
    
    with open(path, 'r') as file:
        raw_data = json.load(file)
       
    # Laatste data-onderdeel niet van belang voor onderzoek  
    for i in range(len(raw_data) - 1): # laatste data onderdeel niet van belang
        if (raw_data[i]["name"] == "as.up.data.forward"):
            uplink = raw_data[i]["data"]["uplink_message"]
            
            
            s_cnt.append(uplink["f_cnt"])
            s_sensor.append(raw_data[i]["data"]["end_device_ids"]["device_id"])
            s_airtime.append(float(uplink["consumed_airtime"].replace('s', '')))
            s_bw.append(uplink["settings"]["data_rate"]["lora"]["bandwidth"])
            s_sf.append(uplink["settings"]["data_rate"]["lora"]["spreading_factor"])
            # 'id' telt op met 2, Application Servers (as). Network Service (ns) geen verschil op waarden
            s_id.append(i)
            
            for j in range(len(uplink["rx_metadata"])):
                d_cnt.append(uplink["f_cnt"])
                d_gateway.append(uplink["rx_metadata"][j]["gateway_ids"]["gateway_id"])
                d_rssi.append(uplink["rx_metadata"][j]["rssi"])
                d_snr.append(uplink["rx_metadata"][j]["snr"])
                d_id.append(i)
                
    df_sensor = pd.DataFrame({'CNT': s_cnt,
                              'SENSOR': s_sensor,
                              'AIRTIME': s_airtime,
                              'BW': s_bw,
                              'SP': s_sf},
                             index=s_id)
    
    df_data = pd.DataFrame({'RSSI': d_rssi,
                            'SNR': d_snr},
                           index=[d_id, d_gateway])
    
    return df_sensor, df_data

AG2AG_SENSOR, AG2AG_DATA = get_json(AG2AG_PATH)
# print(AG2AG_DATA)
# print(AG2AG_SENSOR)

UG2AG_SENSOR, UG2AG_DATA = get_json(UG2AG_PATH)
# print(UG2AG_DATA)
# print(UG2AG_SENSOR)