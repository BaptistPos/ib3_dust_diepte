import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statistics

AG2AG_PATH = "data_02_45\data_200_AG2AG.json"
UG2AG_PATH = "data_02_45\data_200_UG2AG_300mm.json"

def get_json(path):
    s_id, s_cnt, s_sensor, s_airtime, s_bw, s_sf = [], [], [], [], [], []
    d_id, d_cnt, d_gateway, d_rssi, d_snr = [], [], [], [], []
    
    with open(path, 'r') as file:
        raw_data = json.load(file)
       
    # Laatste data-onderdeel niet van belang voor onderzoek  
    for i in range(len(raw_data) - 1):
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

def sensor_rssi_snr(df_data):
    sensor_rssi = {}
    sensor_snr = {}
    
    for i in range(len(df_data.loc[0])):
        sensor_rssi[df_data.loc[0].index[i]] = int(df_data.loc[0]["RSSI"][i])  
        sensor_snr[df_data.loc[0].index[i]] = int(df_data.loc[0]["SNR"][i])
    
    sensor_rssi = dict(sorted(sensor_rssi.items(), key=lambda item: item[0]))
    sensor_snr = dict(sorted(sensor_snr.items(), key=lambda item: item[0]))    
    
    return sensor_rssi, sensor_snr

AG2AG_SENSOR, AG2AG_DATA = get_json(AG2AG_PATH)
UG2AG_SENSOR, UG2AG_DATA = get_json(UG2AG_PATH)

AG2AG_SENSOR_RSSI, AG2AG_SENSOR_SNR = sensor_rssi_snr(AG2AG_DATA)
UG2AG_SENSOR_RSSI, UG2AG_SENSOR_SNR = sensor_rssi_snr(UG2AG_DATA)

target_gateway = ['ttn-vives-indoor-05', 'ttn-vives-indoor-06', 'ttn-vives-indoor-07', 'ttn-vives-indoor-11', 'ttn-vives-indoor-13']

for gateway in target_gateway:
    AG2AG_df_filtered = AG2AG_DATA.xs(gateway, level=1)
    UG2AG_df_filtered = UG2AG_DATA.xs(gateway, level=1)
    
    AG2AG_mean_rssi = round(statistics.mean(AG2AG_df_filtered["RSSI"]), 2)
    AG2AG_mean_snr = round(statistics.mean(AG2AG_df_filtered["SNR"]), 2)
    UG2AG_mean_rssi = round(statistics.mean(UG2AG_df_filtered["RSSI"]), 2)
    UG2AG_mean_snr = round(statistics.mean(UG2AG_df_filtered["SNR"]), 2)
    
    fig, ax1 = plt.subplots()
    plt.title(f'AG2AG vs UG2AG: {gateway}')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.text(0.1, 0.025, f'AG2AG rssi mean: ${AG2AG_mean_rssi}$', fontsize=11, transform=plt.gcf().transFigure, color='b')
    plt.text(0.35, 0.025, f'UG2AG rssi mean: ${UG2AG_mean_rssi}$', fontsize=11, transform=plt.gcf().transFigure, color='r')
    plt.text(0.6, 0.025, f'AG2AG snr mean: ${AG2AG_mean_snr}$', fontsize=11, transform=plt.gcf().transFigure, color='b')
    plt.text(0.85, 0.025, f'UG2AG snr mean: ${UG2AG_mean_snr}$', fontsize=11, transform=plt.gcf().transFigure, color='r')
    
    ax1.set_xlabel('# Pakket')
    ax1.set_ylabel('RSSI [dBm]')
    ax1.plot(AG2AG_df_filtered.index, AG2AG_df_filtered['RSSI'], linestyle='-', color='b', label='AG2AG: RSSI')
    ax1.plot(UG2AG_df_filtered.index, UG2AG_df_filtered['RSSI'], linestyle='-', color='r', label='UG2AG: RSSI')
    
    ax1.set_xlabel('Index')
    ax2 = ax1.twinx()
    ax2.set_yticklabels([])
    ax2.set_ylabel('SNR [dB]')
    ax1.plot(AG2AG_df_filtered.index, AG2AG_df_filtered['SNR'], linestyle='--', color='b', label='AG2AG: SNR')
    ax1.plot(UG2AG_df_filtered.index, UG2AG_df_filtered['SNR'], linestyle='--', color='r', label='UG2AG: SNR')
    ax1.legend()

cnt_air = {'AG2AG_PACKCOUNT': statistics.mean(AG2AG_SENSOR['CNT']), 
           'UG2AG_PACKCOUNT': statistics.mean(UG2AG_SENSOR['CNT']),
           'AG2AG_AIRTIME': statistics.mean(AG2AG_SENSOR['AIRTIME']),
           'UG2AG_AIRTIME': statistics.mean(UG2AG_SENSOR['AIRTIME'])}

s = pd.Series(cnt_air)
s.index = pd.MultiIndex.from_tuples([tuple(idx.split('_')) for idx in s.index])
df = s.unstack()
print(df)
