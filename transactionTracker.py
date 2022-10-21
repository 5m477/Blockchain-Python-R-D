## First Draft Version of MakeMeASandwhich.py by CC labs / Console Cowboys
## @ficti0n on twitter
# From the Console Cowboys Blockchain Forensics Youtube Series (link below)
#https://www.youtube.com/watch?v=LI4PrsqzORE&list=PLCwnLq3tOElrUdIg4LgdhPhCKAiy7NZYA
## Uses the web3.py API to pull down transactions in the latest block
## Then finds likily bot activity and then parses out Frontrunning and Sandwich attacks

import requests, os
from colorama import Fore 
import pyfiglet 

result = pyfiglet.figlet_format("Dexentric Transaction Finder", font ="digital")
print(f'{Fore.RED} 477 scanning for information: \n {Fore.WHITE}{result}')

EthAddresses = [line.rstrip() for line in open('EthAddresses.txt')]
api_key = os.getenv('APIKEY')
total_value_received = 0

for count, target_address in enumerate (EthAddresses):
    value_in_address = 0

    etherscan_params = (
        ('module', 'account'),
        ('action', 'txlistinternal'),
        ('address', target_address),
        ('sort', 'asc'),
        ('apikey', api_key)
    )


    response = requests.get("https://api.etherscan.io/api", params=etherscan_params)

    data = response.json().get("result")

    for ID, transaction in enumerate(data):
        current_value = int(transaction.get("value")) / 1000000000000000000
        print(f'Sending FROM: {transaction.get("from")}')
        print(f'    - Amount: {transaction.get("value")}')
        print(f'MethodID:{transaction.get("methodId")} == {transaction.get("functionName")}')

        total_value_received += current_value
        value_in_address = current_value

    print(f'{Fore.WHITE} Value in: {Fore.RED}{target_address} is {Fore.GREEN}{value_in_address}')
print(f'{Fore.YELLOW} Total Contract Value Received:{Fore.GREEN}{total_value_received}')
