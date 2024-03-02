
import random
from time import sleep
from pprint import pprint
from datetime import datetime
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
    }
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

NETWORK_TREE = [
    [b3l40],
    [b3l40, b2l30],
    [b2l30]
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
    # do some calcu. to find the best path possable
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
    sleep(cost[2] * 0.01)

    print(f'{source} ... BW:{cost[1]}|L:{cost[2]} ... {dist(source, cost[0])}')


# start mapping the network tree
map(tree=NETWORK_TREE)

for i in range(10):
    service = random.choice(SERVICE_TYPES)
    print(f'Need good {service}')
    client('192.168.0.1', random.choice(SERVICE_TYPES), random.choice([youtube, instagram, facebook]), 10, 35)

# pprint(DATABASE)
pprint(COST)





