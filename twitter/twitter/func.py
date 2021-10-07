from django.conf import settings
from django.contrib.auth.models import User
import jwt, requests, json

from rest_framework.response import Response


def cookie_value_to_dict(str):
    data = {}

    # semicolon_indexex = [0]

    cookie_key_value_units = str.split(';')

    for i in cookie_key_value_units:
        dict = cookie_key_value_units_to_dict(i)
        data.update(dict)

    # print(semicolon_indexex, str[256])

    # for i in range(1, len(semicolon_indexex)):
    #     print(i)
    #     dict = till_semicolon_str_to_dict(str[semicolon_indexex[i-1]: semicolon_indexex[i]])
    #     data.update(dict)
    
    # print(data)
    
    # print(str[0: semicolon_indexex[0]])
    # print(semicolon_indexex)

    # if semicolon_index != -1:
    #     dict = till_semicolon_str_to_dict(str[0: semicolon_index])
    #     data.update(dict)
    #     print(dict)
        

    return data

def cookie_key_value_units_to_dict(str):
    dict = {}

    strip_str = str.strip()

    equal_index = strip_str.find('=')

    key_in_str = strip_str[0:equal_index]
    value_in_str = strip_str[equal_index+1:]

    dict[key_in_str] = value_in_str

    return dict

cookie_value_to_dict("token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjMyODU4MjYyLCJqdGkiOiI3NTNkOTJmMjA1NGU0Y2I4OTVkYjgzZDIzMDQ1NjBhZCIsInVzZXJfaWQiOjI2fQ.19PnXIDLO4pp2lupWnpdSTPiqBdMK3AoqTLdYzYTyLhEFCEZ-ZiUulMawy6nmQA6xjpW-w3WG186AuuKYoFSpQ; refresh=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYzMjkzNzQ2MiwianRpIjoiODY5OGI4OWQyZDZjNGJkMDk1M2U2N2YwNTMyZTI5ZTMiLCJ1c2VyX2lkIjoyNn0.aqWQah_7606mc0SMMbKHSym6O13WU4rsslcI8BbPHqCYM2QOk8OBHbWjhwQKnQdh6j_zZffpx_gpfMo9My2MvA; username=shahed")


def auth_user_tokens(dict):
    try:
            
        token = dict['token']
        refresh = dict['refresh']
        username = dict['username']
    except KeyError:
        return 'wrong_specs'

    print(dict)

    key = settings.SECRET_KEY

    # payload = jwt.decode(token, key, algorithms=["HS512"])
    # print(token, 'sldfj')
    
    # user = User.objects.filter(id= payload["user_id"])

    # if user[0].username == username:
    #     print(user[0].id, user[0].username)
    #     return dict
    
    try:

        payload = jwt.decode(token, key, algorithms=["HS512"])

        user = User.objects.filter(id= payload["user_id"])

        if user[0].username == username:
            print(user[0].id, user[0].username)
            return dict
        else:
            return 'wrong_username'

    except jwt.ExpiredSignatureError:
        print('expired: new token')

        url = 'http://127.0.0.1:8000/accounts/token/refresh/'
        data = {'refresh': refresh}
        request = requests.post(url, data=json.dumps(data), headers={'content-type': 'application/json'})
        response_result = request.json()
        dict['token'] = response_result['access']
        # new_access_token = response_result['access']
        # response = Response()
        # response.set_cookie('token', new_access_token, httponly=True)
        return dict
    except jwt.InvalidTokenError:
        return {'error': 'wrong_token'}

    except jwt.exceptions.DecodeError:
        return {'error': 'token_not_correct'}


# auth_user_tokens("token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjMyODU4MjYyLCJqdGkiOiI3NTNkOTJmMjA1NGU0Y2I4OTVkYjgzZDIzMDQ1NjBhZCIsInVzZXJfaWQiOjI2fQ.19PnXIDLO4pp2lupWnpdSTPiqBdMK3AoqTLdYzYTyLhEFCEZ-ZiUulMawy6nmQA6xjpW-w3WG186AuuKYoFSpQ; refresh=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYzMjkzNzQ2MiwianRpIjoiODY5OGI4OWQyZDZjNGJkMDk1M2U2N2YwNTMyZTI5ZTMiLCJ1c2VyX2lkIjoyNn0.aqWQah_7606mc0SMMbKHSym6O13WU4rsslcI8BbPHqCYM2QOk8OBHbWjhwQKnQdh6j_zZffpx_gpfMo9My2MvA; username=shahed")
