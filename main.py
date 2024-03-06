
import random
from time import sleep
from pprint import pprint
from datetime import datetime
import matplotlib.pyplot as plt

# from .facebook import facebook


COST = {
    'raw':[],
}

SERVICE_TYPES = ['bandwidth', 'latency', None]

DATABASE = {
    'youtube': {
        'request': {
            'ip': '',
            'requests': [],
            'vistes': 0,
        }
    },
    'instagram': {
        'request': {
            'ip': '',
            'requests': [],
            'vistes': 0,
        }
    },
    'facebook': {
        'request': {
            'ip': '',
            'requests': [],
            'vistes': 0,
        }
    },
    'b3l40': {
        'passthrough': {
            'ip': '',
            'vistes': 0,
        }
    },
    'Twitter': {
        'request': {
            'ip': '',
            'requests': [],
            'vistes': 0,
        }
    },
    'Reddit': {
        'request': {
            'ip': '',
            'requests': [],
            'vistes': 0,
        }
    },
}

def serverlog(name, clientip, path):
    DATABASE[name]['request']['ip'] = clientip
    DATABASE[name]['request']['requests'].append([clientip, path, datetime.now().strftime("%Y/%m/%d-%H:%M:%S")])
    DATABASE[name]['request']['vistes'] += 1

# server
def youtube(clientip, path):
    serverlog('youtube', clientip, path)
    return 'Youtube'

# server
def instagram(clientip, path):
    serverlog('instagram', clientip, path)
    return 'Instagram'

# server
def facebook(clientip, path):
    serverlog('facebook', clientip, path)
    return 'Facebook'

# nodes in between
def b2l30():
    return [2, 30]

def b3l40():
    # return 'bandwidth 3 mb and  Latency 40 ms'
    return [3, 40]
def b5l60():
    # return 'bandwidth 5 mb and Latency 60 ms'
    return [5, 60]

def b2l25():
    # return 'bandwidth 2 mb and Latency 25 ms'
    return [2, 25]

def b6l70():
    # return 'bandwidth 6 mb and Latency 70 ms'
    return [6, 70]

def b3l30():
    # return 'bandwidth 3 mb and Latency 30 ms'
    return [3, 30]

def b7l80():
    # return 'bandwidth 7 mb and Latency 80 ms'
    return [7, 80]

def b4l35():
    # return 'bandwidth 4 mb and Latency 35 ms'
    return [4, 35]

def b8l90():
    # return 'bandwidth 8 mb and Latency 90 ms'
    return [8, 90]

def b9l100():
    # return 'bandwidth 9 mb and Latency 100 ms'
    return [9, 100]

def b10l110():
    # return 'bandwidth 10 mb and Latency 110 ms'
    return [10, 110]

def b11l120():
    # return 'bandwidth 11 mb and Latency 120 ms'
    return [11, 120]

NETWORK_TREE = [
    [b3l40],
    [b3l40, b2l30],
    [b2l30],
    [b5l60],
    [b5l60, b2l25],
    [b6l70],
    [b6l70, b3l30],
    [b7l80],
    [b7l80, b4l35],
    [b8l90],
    [b8l90, b9l100],
    [b10l110],
    [b10l110, b11l120]
]
def sortpaths(path, via):
     
    if via == 'bandwidth':
        path = sorted(path, key=lambda x: x[1])
        return list(reversed(path))
    elif via == 'latency':
        return sorted(path, key=lambda x: x[2])

def map(tree=NETWORK_TREE):
    bandwidth = 0
    latency = 0
    for path in tree:
        for node in path:
            bandwidth += node()[0]
            latency += node()[1]

        print(f'{[fn.__name__ for fn in path]} --- bandwidth : {bandwidth} , latency : {latency}')

        COST['raw'].append([path, bandwidth, latency])

        bandwidth = 0
        latency = 0

    COST['bandwith_sorted'] = sortpaths(COST['raw'], 'bandwidth')
    COST['latency_sorted'] = sortpaths(COST['raw'], 'latency')

def bp(service_type, size, max_latency):
    # do some calcu. to find the best path possible
    # [client, b3l40, b2l30, server]

    # return random.choice([[b3l40()],
    #                       [b3l40(), b2l30()],
    #                       [b2l30()]])

    if service_type == 'bandwidth':
        return COST['bandwith_sorted'][0]
    elif service_type == 'latency':
        return COST['latency_sorted'][0]
    else:
        return COST['bandwith_sorted'][0]

def request(ip):
    return f'Device{ip}'

# client
def client(source='', service_type=None, dist=youtube, size=3, max_latency=100):

    """
    distnation  : server
    size        : estmiated requested data size in mb
    max_latency : max latency allowed for user experience
    """

    request(source)

    cost = bp(service_type, size, max_latency)

    # delay
    sleep(cost[2] * 0.001)

    print(f'{source} ... BW:{cost[1]}|L:{cost[2]} ... {dist(source, cost[0])}')


# start mapping the network tree
map(tree=NETWORK_TREE)

for i in range(50):
    service = random.choice(SERVICE_TYPES)
    print(f'Need good {service}')
    client('192.168.0.1', random.choice(SERVICE_TYPES), random.choice([youtube, instagram, facebook]), 10, 35)

# pprint(DATABASE)
pprint(COST)



# Get service names and their corresponding number of requests, bandwidth, and latency
services = []
num_requests = []
bandwidths = []
latencies = []

for service, data in DATABASE.items():
    if 'request' in data:
        services.append(service)
        num_requests.append(data['request'].get('vistes', 0))
        # Assuming bandwidth and latency information is available in the database
        bandwidths.append(data['request'].get('bandwidth', 0))
        latencies.append(data['request'].get('latency', 0))

# Extract bandwidth and latency values from NETWORK_TREE
paths_bandwidth = []
paths_latency = []

for path in NETWORK_TREE:
    bandwidth = sum(node()[0] for node in path)
    latency = sum(node()[1] for node in path)
    paths_bandwidth.append(bandwidth)
    paths_latency.append(latency)

# Plot each request
plt.figure(figsize=(10, 6))
for service, data in DATABASE.items():
    if 'request' in data:
        # Extract bandwidth and latency values for the path taken by the request
        bandwidth = paths_bandwidth[services.index(service)]
        latency = paths_latency[services.index(service)]
        # Plot the request with bandwidth and latency as coordinates
        plt.scatter(bandwidth, latency, label=service, s=data['request']['vistes']*10)  # Adjust the size of the point based on the number of requests
        plt.text(bandwidth, latency, service, fontsize=8, ha='right', va='bottom')

plt.xlabel('Bandwidth')
plt.ylabel('Latency')
plt.title('Bandwidth vs Latency for Each Request')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()