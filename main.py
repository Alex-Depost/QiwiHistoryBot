import requests
from time import sleep
import configparser
import telebot

config = configparser.ConfigParser()
config.read("config.ini")

Token = config['Qiwi']['Token']
Login = config['Qiwi']['Login']
BotToken = config['Qiwi']['BotToken']

users = open("users.txt", 'r')
users = users.read().splitlines()

bot = telebot.TeleBot(BotToken)


def payment_history_last(my_Login, api_access_token, rows_num):
    s = requests.Session()
    s.headers['authorization'] = 'Bearer ' + api_access_token
    parameters = {'rows': rows_num}
    h = s.get('https://edge.qiwi.com/payment-history/v2/persons/' + my_Login + '/payments', params=parameters)
    return h.json()


def GenerateMessage(PaymentInfo):
    res = "На сумму {}\n" \
          "С {}\n" \
          "От {}\n" \
          "Комментарий: {}".format(PaymentInfo['total']['amount'], PaymentInfo['view']['title'],
                                   PaymentInfo['view']['account'], PaymentInfo['comment'])
    return res


LastPay = payment_history_last(Login, Token, 1)['data'][0]

while True:
    NewPay = payment_history_last(Login, Token, 1)['data'][0]
    if LastPay['txnId'] != NewPay['txnId']:
        if NewPay['type'] == 'IN' and NewPay['status'] == 'SUCCESS':
            for elem in users:
                bot.send_message(elem, "✅Новый перевод✅")
                bot.send_message(elem, GenerateMessage(NewPay))
                print("✅Новый перевод✅")
                print(GenerateMessage(NewPay))
            LastPay = NewPay
    sleep(1)
