import requests

# Полная и актуальная документация по API: https://calltools.ru/guide_api


CALLTOOLS_PUBLIC_KEY = '7412029812f124b3b30708d28661f9fb'
CALLTOOLS_BASE_URL = 'https://zvonok.com'
CALLTOOLS_TIMEOUT = 30


class CallToolsException(Exception):
    pass


def create_call(campaign_id, phonenumber, text=None, speaker='Tatyana'):

    resp = requests.get(CALLTOOLS_BASE_URL + '/manager/cabapi_external/api/v1/phones/call/', {
        'public_key': CALLTOOLS_PUBLIC_KEY,
        'phone': phonenumber,
        'campaign_id': campaign_id,
        'text': text,
        'speaker': speaker,
    }, timeout=CALLTOOLS_TIMEOUT)
    ret = resp.json()
    print(ret)
    if ret['status'] == 'error':
        raise CallToolsException(ret['data'])
    return ret

if __name__ == '__main__':
    create_call(campaign_id=1331539899, phonenumber='+79112972946', text='Поступил новый заказ', speaker='Tatyana')