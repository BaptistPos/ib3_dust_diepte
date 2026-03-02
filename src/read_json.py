import json

with open('data/data_huis_trap.json', 'r') as file:
    raw_data = json.load(file)

for i in range(len(raw_data) - 1):
    if (raw_data[i]["name"] == "as.up.data.forward"):
        print(f"Sensor ({json.dumps(raw_data[i]["data"]["uplink_message"]["f_cnt"])}, {json.dumps(raw_data[i]["data"]["uplink_message"]["consumed_airtime"])}): {json.dumps(raw_data[i]["data"]["end_device_ids"]["device_id"])})")
        for j in range(len(raw_data[i]["data"]["uplink_message"]["rx_metadata"])):
            print("\tGateway: " + json.dumps(raw_data[i]["data"]["uplink_message"]["rx_metadata"][j]["gateway_ids"]["gateway_id"]))
            print("\t\tRSSI: " + json.dumps(raw_data[i]["data"]["uplink_message"]["rx_metadata"][j]["rssi"]))
            print("\t\tSNR: " + json.dumps(raw_data[i]["data"]["uplink_message"]["rx_metadata"][j]["snr"]))
            print("\t\tReceived: " + json.dumps(raw_data[i]["data"]["uplink_message"]["rx_metadata"][j]["received_at"]))
        print("\n")



