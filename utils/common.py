import requests
from models.setting import Setting
from base64 import b64decode
from json import dumps


def json_build_object(*args):
    pairs = []
    for i in range(0, len(args), 2):
        key = args[i]
        value = args[i + 1]
        pairs.append(f'"{key}": "{value}"')
    return '{' + ', '.join(pairs) + '}'


def login():
    host = Setting.find_by_key('api_url')
    # host = 'http://172.17.0.1:1001'
    setting = Setting.get_list()
    code = next(filter(lambda x: x['key'] == 'code', setting))
    password = next(filter(lambda x: x['key'] == 'password', setting))
    code = code['value']
    password = b64decode(password['value'].encode()).decode()
    response = requests.post(f'{host}/login', dumps({'code': code, 'password': password}))
    response = response.json()
    if 'access' in response:
        token = response['access']
        return token
    return None


def to_current(raw_value):
    min_value = 4000
    max_value = 20000
    min_current = 0
    max_current = 50
    if min_value <= raw_value <= max_value:
        rate = (raw_value - min_value) / (max_value - min_value)
        return (max_current - min_current) * rate

    return None
