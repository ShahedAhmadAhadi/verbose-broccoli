from django.conf import settings
from django.contrib.auth.models import User
import jwt, requests, json
from jwt import exceptions

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
        print(dict)
    except KeyError:
        return 'wrong_specs'

    key = settings.SECRET_KEY
    
    try:
        payload = jwt.decode(token, key, algorithms=["HS512"])

        user = User.objects.filter(id= payload["user_id"])

        if user[0].id == username:
            print(user[0].id, user[0].username)
            # response = Response()
            return dict
        else:
            return 'wrong_username'

    except jwt.ExpiredSignatureError:
        print('expired: new token')

        url = 'http://127.0.0.1:8000/accounts/token/refresh/'
        data = {'refresh': refresh}
        request = requests.post(url, data=json.dumps(data), headers={'content-type': 'application/json'})
        response_result = request.json()
        try: 
            # token_dict = response_result['access']
            dict['token'] = response_result['access']
            return dict
        except KeyError:
            dict = {}
            dict.update(response_result)
            return dict
        # new_access_token = response_result['access']
        # response = Response()
        # response.set_cookie('token', new_access_token, httponly=True)

    except jwt.InvalidTokenError:
        return 'not_valid_token'


def auth_user_request(request):

    http_cookie = request.META.get("HTTP_COOKIE")
    response = Response()
    # auth_info_dict = cookie_value_to_dict(http_cookie)
    try:
        auth_info_dict = cookie_value_to_dict(http_cookie)

    except AttributeError:
        response.data = {'error': 'no_validations'}
        return {'response': response, 'condition': False}

    auths = auth_user_tokens(auth_info_dict)

    try:
        response.set_cookie('token', auths['token'], httponly=True)
        # response.set_cookie('username', 'shahed', httponly=True)
        data = auths
        print(auths, 'try')
        return {'response': response, 'condition': True, 'data': data}
    except:
        response.data = auths
        print(auths, 'except')
        response.delete_cookie('token')
        response.delete_cookie('refresh')
        response.delete_cookie('username')
        return {'response': response, 'condition': False}
    #     if type(auths) == dict:
    #     # response.set_cookie(, httponly=True)
    #         response.data = auths
    #         print(auths, 'except')
    #         response.delete_cookie('token')
    #         response.delete_cookie('refresh')
    #         response.delete_cookie('username')
    #         return {'response': response, 'condition': False}
    #     else:
    #         response.data = auths
    #         response.delete_cookie('token')
    #         response.delete_cookie('refresh')
    #         response.delete_cookie('username')
    #         return {'response': response, 'condition': False}
    
    # # response = Response({'auths': 'auths'})
    # print(auths)

    # return {'response': Response('a'), 'condition': True}
    # Response(request)


