import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import random

# Constants
num_nodes = 30
servers = ['Instagram', 'YouTube', 'Facebook', 'IoTDevices', 'RoN']


total_bandwidth_gigabit = float(input("Enter total bandwidth in gigabits: "))
bandwidth_split = [float(input(f"Enter bandwidth split for {server} in percentage: ")) for server in servers]
bandwidth_split = [split / 100 * total_bandwidth_gigabit for split in bandwidth_split]


G = nx.DiGraph()


connection_details = []


for node in range(1, num_nodes + 1):
    server = random.choice(servers)
    latency = random.uniform(70, 140)
    bandwidth = random.choice(bandwidth_split)
    G.add_edge(node, server, latency=latency, bandwidth=bandwidth)
    connection_details.append({'Node': node, 'Server': server, 'Latency': latency, 'Bandwidth': bandwidth})


connection_df = pd.DataFrame(connection_details)


download_details = []
for index, row in connection_df.iterrows():
    file_size = random.uniform(4, 7)
    time_to_download = file_size / row['Bandwidth']
    download_details.append({'Node': row['Node'], 'Server': row['Server'], 'File_Size_GB': file_size, 'Time_to_Download_sec': time_to_download})

download_df = pd.DataFrame(download_details)
final_df = pd.merge(connection_df, download_df, on=['Node', 'Server'])

final_df.to_csv('connection_details.csv', index=False)


fig, ax = plt.subplots(figsize=(12, 8))

bar_width = 0.25
index = range(len(final_df))

latency_bar = ax.bar(index, final_df['Latency'], bar_width, label='Latency', alpha=0.7)
bandwidth_bar = ax.bar([i + bar_width for i in index], final_df['Bandwidth'], bar_width, label='Bandwidth', alpha=0.7)
download_time_bar = ax.bar([i + 2 * bar_width for i in index], final_df['Time_to_Download_sec'], bar_width, label='Download Time', alpha=0.7)

ax.set_xlabel('Connections')
ax.set_ylabel('Values')
ax.set_title('Network Simulation Bar Chart')
ax.set_xticks([i + bar_width for i in index])
ax.set_xticklabels(final_df['Node'].astype(str) + ' to ' + final_df['Server'])
ax.legend()

plt.show()
