import requests
import json

def get_kurs(value):
    json_object = requests.get(f'https://api.tinkoff.ru/v1/currency_rates?from={value}&to=RUB').json()

    for value in json_object['payload']['rates']:
        for k, v in value.items():
            if v == 'DebitCardsTransfers':
                return (f'продажа: {value["buy"]} рублей, покупка: {value["sell"]} рублей')

