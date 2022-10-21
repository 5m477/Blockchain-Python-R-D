## First Draft Version of MakeMeASandwhich.py by CC labs / Console Cowboys
## @ficti0n on twitter
# From the Console Cowboys Blockchain Forensics Youtube Series (link below)
#https://www.youtube.com/watch?v=LI4PrsqzORE&list=PLCwnLq3tOElrUdIg4LgdhPhCKAiy7NZYA
## Uses the web3.py API to pull down transactions in the latest block
## Then finds likily bot activity and then parses out Frontrunning and Sandwich attacks

from web3 import Web3
from colorama import Fore

import pyfiglet

result = pyfiglet.figlet_format("Dexentric Bot Sandwich Tracker", font ="ogre")
print(f'{Fore.GREEN}477 Searching for Sandwich: \n {Fore.RED}{result}') 

web3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/<"APIKEY">'))
block = web3.eth.get_block('latest')
toFromPairs = {}
transactionCount = {}
txLookup = {}
possibleSandwich = {}

def grabTransactions():
    if block and block.transactions: 
        for transaction in block.transactions: 
            tx_hash = transaction.hex() # Convert txhashes from hexBytes format
            tx = web3.eth.get_transaction(tx_hash)
            
            if tx.to != None:
                if tx.to in toFromPairs:
                    if toFromPairs[tx.to] == tx["from"]:
                        transactionCount[tx.to] = transactionCount[tx.to] +1 
                        txLookup[tx_hash] =  [tx.to,tx["from"],tx.gasPrice]
                        
                elif tx.to not in toFromPairs:
                    transactionCount[tx.to] = 1
                    toFromPairs[tx.to] = tx["from"]
                    txLookup[tx_hash] =  [tx.to,tx["from"],tx.gasPrice]

              
def findBots():
    for transactionHash, pair in txLookup.items():    
        if transactionCount[pair[0]] == 2:
            possibleSandwich[transactionHash] = [pair[0],pair[2]]   

            
def findSandwich(possibleSandwich): 
    allBots = {}
    duplicateBots = {}
    sandwiches = []

    for sHash, sGas in possibleSandwich.items(): 
        if sGas[1] in allBots.values():
            duplicateBots[sHash] = sGas[1]
        
        elif sGas[1] not in allBots.values():    
            allBots[sHash] = sGas[1]
            
    print(f'{len(allBots)} bot transactions parsed with 2 like pairs')
    print('---------------------------------------------------------')
    for bot in allBots.keys():
        print(bot)
    print('---------------------------------------------------------')


    for sHash, bot in allBots.items():
        if duplicateBots:
            if bot not in duplicateBots.values():
               sandwiches.append(sHash) 

    return sandwiches           
 

if __name__ == "__main__":
    grabTransactions()
    findBots()

    if possibleSandwich:
        sandwiches =findSandwich(possibleSandwich)
        for sandwich in sandwiches:
            print(f'{Fore.GREEN}Delicious Sandwich Found: \n {Fore.YELLOW}{sandwich}')        
            
