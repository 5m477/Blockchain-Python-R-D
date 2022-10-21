## First Draft Version of MakeMeASandwhich.py by CC labs / Console Cowboys
## @ficti0n on twitter
# From the Console Cowboys Blockchain Forensics Youtube Series (link below)
#https://www.youtube.com/watch?v=LI4PrsqzORE&list=PLCwnLq3tOElrUdIg4LgdhPhCKAiy7NZYA
## Uses the web3.py API to pull down transactions in the latest block
## Then finds likily bot activity and then parses out Frontrunning and Sandwich attacks

from web3 import Web3
import pyfiglet

result = pyfiglet.figlet_format("477 BotTracker", font ="digital")
print(result)

web3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/<"APIKEY">'))
block = web3.eth.get_block('latest')
toFromPairs = {}
transactionCount = {}

if block and block.transactions: 
    for transaction in block.transactions: 
        tx_hash = transaction.hex() # Convert txhashes from hexBytes format
        tx = web3.eth.get_transaction(tx_hash)

        if tx.to != None:
            if tx.to in toFromPairs:
                if toFromPairs[tx.to] == tx["from"]:
                    transactionCount[tx.to] = transactionCount[tx.to] +1 

            elif tx.to not in toFromPairs:
                transactionCount[tx.to] = 1
                toFromPairs[tx.to] = tx["from"]


for key, value in transactionCount.items():
    if value == 2:
        print(toFromPairs[key])
