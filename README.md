# Token Checker
Mini app fetching token balances for a given wallet address. 
Currently supports only ETH chain. 

## Features
Wallet Balance Retrieval: The application offers two endpoints for obtaining the balance of a specified Ethereum wallet. The first endpoint retrieves the balance through direct contract calls to the Ethereum network, while the second endpoint utilizes the Ethplorer API for balance retrieval.

## Environment Variables
The application uses the following environment variables:

**INFURA_API_KEY:** Your Infura API key. This is used to connect to the Ethereum network.
**ETHPLORER_API_KEY:** Your Ethplorer API key. This is used to fetch data from the Ethplorer API.

## ERC20_ABI
The application includes the ABI (Application Binary Interface) for ERC20 tokens. This ABI is used to interact with ERC20 token contracts on the Ethereum network. It includes the balanceOf, decimals, and symbol functions.

## Installation
Python and pip must be intalled on your platform. 
To install the necessary packages for this script, use pip:

    pip install web3
    pip install flask
    pip install python-dotenv
    pip install pandas
    pip install requests

## Usage
To start the application, run the following command:

    py checker.py


## API Documentation

This Python script provides two API endpoints for fetching Ethereum wallet balances.

### Direct Balance Fetch

Uses whitelist for token contracts. Resource: [etherscan.io](https://etherscan.io/exportData?type=open-source-contract-codes)

**Endpoint:** /direct/balance/{wallet}

**Method:** GET

**Description:** This endpoint returns the balance of a given Ethereum wallet by making direct contract calls to the Ethereum network.

#### Parameters:

**wallet:** The Ethereum wallet address.

#### Query Parameters:

**chain:** The blockchain network to use. Defaults to 'eth'. `!Note: currently only Ethereum is supported` 

**limit:** The maximum number of tokens to fetch. Must be an integer between 1 and 10000. Defaults to 10.

**Response:** A JSON object containing the balances of all tokens in the wallet. Each key is a token symbol and the corresponding value is the balance of that token.

### Ethplorer API Balance Fetch

No whitelist used for this approach, returns all tokens that have non-zero balance for a given wallet address. `!Note: may return scam tokens as well` 

**Endpoint:** /api/balance/{wallet}

**Method:** GET

**Description:** This endpoint returns the balance of a given Ethereum wallet by fetching data from the Ethplorer API.

#### Parameters:

**wallet:** The Ethereum wallet address.

**Response:** A JSON object containing the balances of all tokens in the wallet. Each key is a token symbol and the corresponding value is the balance of that token.


#### Response example:

    {
        "ETH": 0.123456789,
        "DAI": 456.789,
        "USDT": 123456.789
    }