import requests
from models.setting import Setting
from base64 import b64decode


def json_build_object(*args):
    pairs = []
    for i in range(0, len(args), 2):
        key = args[i]
        value = args[i + 1]
        pairs.append(f'"{key}": "{value}"')
    return '{' + ', '.join(pairs) + '}'


def login():
    host = 'http://172.17.0.1:1001/login/'
    setting = Setting.get_list()
    code = next(filter(lambda x: x['key'] == 'code', setting))
    password = next(filter(lambda x: x['key'] == 'password', setting))
    code = code['value']
    password = b64decode(password['value'].encode()).decode()
    response = requests.post(host, {'code': code, 'password': password})
    response = response.json()
    if 'access' in response:
        token = response['access']
        print(token)
