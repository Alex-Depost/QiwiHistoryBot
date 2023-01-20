import requests

token = ""
login = ""


def payment_history_last(my_login, api_access_token, rows_num):
    s = requests.Session()
    s.headers['authorization'] = 'Bearer ' + api_access_token
    parameters = {'rows': rows_num}
    h = s.get('https://edge.qiwi.com/payment-history/v2/persons/' + my_login + '/payments', params=parameters)
    return h.json()


Lastpay = payment_history_last(login, token, 1)

print(Lastpay)
