from web3 import Web3
import pyfiglet

result = pyfiglet.figlet_format("Dexentric BotTracker", font ="digital")
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
