def cookie_value_to_dict(str):
    data = {}

    semicolon_index = str.find(';')
    if semicolon_index != -1:
        dict = till_semicolon_str_to_dict(str[0: semicolon_index])
        data.update(dict)
        print(dict)
        

    return None

def till_semicolon_str_to_dict(str):
    dict = {}

    equal_index = str.find('=')

    key_in_str = str[0:equal_index]
    value_in_str = str[equal_index+1:]

    dict[key_in_str] = value_in_str

    return dict

cookie_value_to_dict("token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjMyODU4MjYyLCJqdGkiOiI3NTNkOTJmMjA1NGU0Y2I4OTVkYjgzZDIzMDQ1NjBhZCIsInVzZXJfaWQiOjI2fQ.19PnXIDLO4pp2lupWnpdSTPiqBdMK3AoqTLdYzYTyLhEFCEZ-ZiUulMawy6nmQA6xjpW-w3WG186AuuKYoFSpQ; refresh=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYzMjkzNzQ2MiwianRpIjoiODY5OGI4OWQyZDZjNGJkMDk1M2U2N2YwNTMyZTI5ZTMiLCJ1c2VyX2lkIjoyNn0.aqWQah_7606mc0SMMbKHSym6O13WU4rsslcI8BbPHqCYM2QOk8OBHbWjhwQKnQdh6j_zZffpx_gpfMo9My2MvA; username=shahed")

def previous_char_str(str):
    for i in str:
        pass

# cookie_value_to_str('sdlfjr')
