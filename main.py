
import random
from time import sleep
from pprint import pprint
from datetime import datetime
# from .facebook import facebook

database = {
    'youtube': {
        'request': {
            'ip': '',
            'route': {'path':[], 'time': datetime},
            'vistes': 0,
        }
    },
    'instagram': {
        'request': {
            'ip': '',
            'route': {'path':[], 'time': datetime},
            'vistes': 0,
        }
    },
    'facebook': {
        'request': {
            'ip': '',
            'route': {'path':[], 'time': datetime},
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

# server
def youtube(clientip, path):
    database['youtube']['request']['ip'] = clientip
    database['youtube']['request']['route']['path'] = path
    database['youtube']['request']['route']['time'] = datetime.now().strftime("%m/%d/%Y-%H:%M:%S")
    database['youtube']['request']['vistes'] += 1
    return 'Youtube'

# server
def instagram(clientip, path):
    database['instagram']['request']['ip'] = clientip
    database['instagram']['request']['route']['path'] = path
    database['instagram']['request']['route']['time'] = datetime.now().strftime("%m/%d/%Y-%H:%M:%S")
    database['instagram']['request']['vistes'] += 1
    return 'Instagram'

# server
def facebook(clientip, path):
    database['facebook']['request']['ip'] = clientip
    database['facebook']['request']['route']['path'] = path
    database['facebook']['request']['route']['time'] = datetime.now().strftime("%m/%d/%Y-%H:%M:%S")
    database['facebook']['request']['vistes'] += 1
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
    x = random.randint(-1, 2)

    if x == 0:
        return [b3l40()]
    elif x == 1:
        return [b3l40(), b2l30()]
    return [b2l30()]


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





