import requests
import json
def call_to_phone():
    data = {"apiKey": "fyfFBv4JWYv5ekZYmsaGi8C2OAqDu8zIlnSV95aRfDn3OnyaADSvkpydDvgR",
            "phone":"79817825035",
            "outgoingPhone":"79802578252",
            "record": {"id": 2674961},
            "ivrs":[{"digit": 1,"needBlock": 0,"smsText": "текст СМС"}]}
    headers = {'Content-Type': 'application/json'}


    response = requests.post('https://lk.calldog.ru/apiCalls/create', data=json.dumps(data), headers=headers)
    print(response.text)