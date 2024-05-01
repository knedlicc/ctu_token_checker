from web3 import Web3
from flask import Flask, request
import os
from dotenv import load_dotenv
import pandas as pd
import requests

load_dotenv()

app = Flask(__name__)

INFURA_API_KEY = os.getenv("INFURA_API_KEY")
ETHPLORER_API_KEY = os.getenv("ETHPLORER_API_KEY")


ERC20_ABI = [
    # balanceOf
    {
        "constant": True,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "type": "function"
    },
    # decimals
    {
        "constant": True,
        "inputs": [],
        "name": "decimals",
        "outputs": [{"name": "", "type": "uint8"}],
        "type": "function"
    },
    # symbol
    {
        "constant": True,
        "inputs": [],
        "name": "symbol",
        "outputs": [{"name": "", "type": "string"}],
        "type": "function"
    }
]

# Get the balance of a wallet on a specific chain by direct contract calls
@app.route('/direct/balance/<wallet>', methods=['GET'])
def get_balances_direct(wallet):    
    chain, limit = validate_parameters_and_set_defaults(request.args.get('chain'), request.args.get('limit'))
    balances = {}
    
    try:
        if chain == 'eth':
            whitelist = fill_whitelist('export-verified-contractaddress-opensource-license.csv',limit)
            web3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/' + INFURA_API_KEY))
            eth_balance = web3.eth.get_balance(wallet)
            balances['ETH'] = float(web3.from_wei(eth_balance, 'ether'))
            for index, token in enumerate(whitelist):
                if(index == limit):
                    break
                token = Web3.to_checksum_address(token)
                contract = web3.eth.contract(address=token, abi=ERC20_ABI)
                try:
                    ticker = contract.functions.symbol().call()     
                    result = contract.functions.balanceOf(wallet).call()
                    decimals = contract.functions.decimals().call()      
                except Exception as e:
                    print(e)
                    print(f'Error fetching token data: ', token)
                    continue
                balances[ticker] = result / (10 ** decimals)
        else: 
            return {'error': 'Chain not supported'}, 400   
    except Exception as e:
        print(e)
        return {'error': 'Error fetching balances'}, 500
    
    return balances
    
# Get the balance of a wallet on a ETH chain by using Ethplorer API
@app.route('/api/balance/<wallet>', methods=['GET'])
def get_balances_api(wallet):
    balances = {}
    
    try:
        response = requests.get(f'https://api.ethplorer.io/getAddressInfo/{wallet}?apiKey={ETHPLORER_API_KEY}')
        response.raise_for_status()
        data = response.json()
        balances['ETH'] = data['ETH']['balance']
        
        for token_info in data['tokens']:
            token = token_info['tokenInfo']
            balances[token['symbol']] = token_info['balance'] / (10 ** int(token['decimals']))
    except Exception as e:
        print(e)
        return {'error': 'Error fetching balances'}, 500
    
    return balances

# Validate the parameters and set the defaults if necessary
def validate_parameters_and_set_defaults(chain, limit):
    if chain == None:
        chain = 'eth'
        print('Chain not specified, defaulting to ETH')
        
    if limit is not None:
        try: 
            limit = int(limit)
        except ValueError:
            return {'error': 'Limit must be an integer'}, 400
        if limit < 1 and limit > 10000:
            return {'error': 'Limit must be greater than 0 and less than 10000'}, 400
    else:
        limit = 10
        print('Limit not specified, defaulting to 10')
    
    return chain, limit
    
# Fill and get the whitelist with the contract addresses from the CSV file
def fill_whitelist(filename, limit):
    whitelist = []
    df = pd.read_csv(filename, skiprows=2, header=None)
    for index, row in df.iterrows():
        if index == limit:
            break
        whitelist.append(row[1])  # Assuming the contract address is in the second column
    return whitelist

# Run the app
if __name__ == '__main__':
    app.run(port=3000)