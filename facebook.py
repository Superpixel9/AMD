
# server
def facebook(clientip, path):
    database['facebook']['request']['ip'] = clientip
    database['facebook']['request']['route']['path'] = path
    database['facebook']['request']['route']['time'] = datetime.now().strftime("%m/%d/%Y-%H:%M:%S")
    database['facebook']['request']['vistes'] += 1
    return 'Facebook'
