
import random
from time import sleep
from pprint import pprint
from datetime import datetime
# from .facebook import facebook

database = {
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
    database[name]['request']['ip'] = clientip
    database[name]['request']['requests'].append([clientip, path, datetime.now().strftime("%Y/%m/%d-%H:%M:%S")])
    database[name]['request']['vistes'] += 1

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
    # return 'Bandwith 3 mb and  Latency 40 ms'
    return [3, 40]

# client
def client(ip):
    return f'Device{ip}'

def bp(size, max_latency):
    # do some calcu. to find the best path possable
    # [client, b3l40, b2l30, server]
    return random.choice([[b3l40()], [b3l40(), b2l30()], [b2l30()]])


def request(source='', dist=youtube, size=3, max_latency=100):

    """
    distnation  : server
    size        : estmiated requested data size in mb
    max_latency : max latency allowed for user experience
    """

    client(source)

    path_list = bp(size, max_latency)

    cost = {'bandwith':0, 'latency':0}

    for p in path_list:
        cost['bandwith'] += p[0]
        cost['latency'] += p[1]

    # delay
    sleep(cost['latency'] * 0.01)

    print(f'{source} ... {cost} ... {dist(source, path_list)}')

for i in range(10):
    request('192.168.0.1', random.choice([youtube, instagram, facebook]), 10, 35)

pprint(database)





