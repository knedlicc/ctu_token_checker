from web3 import Web3
from flask import Flask, request
import os
from dotenv import load_dotenv
import pandas as pd
import requests
from moralis import evm_api
load_dotenv()

app = Flask(__name__)

INFURA_API_KEY = os.getenv("INFURA_API_KEY")
ETHPLORER_API_KEY = os.getenv("ETHPLORER_API_KEY")
MORALIS_API_KEY = os.getenv("MORALIS_API_KEY")


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

# Get a list of top 100 tokens by market cap
@app.route('/moralis', methods=['GET'])
def get_tokens_moralis():
    return evm_api.market_data.get_top_erc20_tokens_by_market_cap(api_key=MORALIS_API_KEY)
    


# Get the balance of a wallet on a specific chain by direct contract calls
@app.route('/direct/balance/<wallet>', methods=['GET'])
def get_balances_direct(wallet):    
    chain, limit = validate_parameters_and_set_defaults(request.args.get('chain'), request.args.get('limit'))
    result = {}
    balances = {}
    total_value = 0
    try:
        if chain == 'eth':
            top_token_list = get_tokens_moralis()
            web3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/' + INFURA_API_KEY))
            eth_balance = web3.eth.get_balance(wallet)
            balances['ETH'] = float(web3.from_wei(eth_balance, 'ether'))
            total_value += balances['ETH'] * float(top_token_list[0]['price_usd'])
            
            for index, token in enumerate(top_token_list):
                if(index == limit):
                    break
                token_address = Web3.to_checksum_address(token['contract_address'])
                contract = web3.eth.contract(address=token_address, abi=ERC20_ABI)
                try:
                    ticker = contract.functions.symbol().call()     
                    balance = contract.functions.balanceOf(wallet).call()
                    decimals = contract.functions.decimals().call()      
                except Exception as e:
                    print(e)
                    print(f'Error fetching token data: ', token)
                    continue
                amount = balance / (10 ** decimals)
                price = token['price_usd']
                balances[ticker] = amount
                total_value += amount * float(price)
        else: 
            return {'error': 'Chain not supported'}, 400   
    except Exception as e:
        print(e)
        return {'error': 'Error fetching balances'}, 500
    
    result['total_value'] = total_value
    result['balances'] = balances
    return result
    
# Get the balance of a wallet on a ETH chain by using Ethplorer API
@app.route('/api/balance/<wallet>', methods=['GET'])
def get_balances_api(wallet):
    result = {}
    balances = {}
    total_value = 0
    try:
        response = requests.get(f'https://api.ethplorer.io/getAddressInfo/{wallet}?apiKey={ETHPLORER_API_KEY}')
        response.raise_for_status()
        data = response.json()
        balances['ETH'] = data['ETH']['balance']
        total_value += balances['ETH'] * data['ETH']['price']['rate']
        for token_info in data['tokens']:
            token = token_info['tokenInfo']
            amount = token_info['balance'] / (10 ** int(token['decimals']))
            if token['price'] == False:
                continue
            price = token['price']['rate']
            balances[token['symbol']] = amount
            total_value += amount * price
    except Exception as e:
        print(e)
        return {'error': 'Error fetching balances'}, 500
    
    result['total_value'] = total_value
    result['balances'] = balances
    return result

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