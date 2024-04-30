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

### 1. Direct Balance Fetch

Uses whitelist for token contracts. Resource: [etherscan.io](https://etherscan.io/exportData?type=open-source-contract-codes)

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**Endpoint:** /direct/balance/{wallet}

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**Method:** GET

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**Description:** This endpoint returns the balance of a given Ethereum wallet by making direct contract calls to the Ethereum network.

#### Parameters:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**wallet:** The Ethereum wallet address.

#### Query Parameters:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**chain:** The blockchain network to use. Defaults to 'eth'. `!Note: currently only Ethereum is supported` 

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**limit:** The maximum number of tokens to fetch. Must be an integer between 1 and 10000. Defaults to 10.

**Request:** GET /direct/balance/0x40B38765696e3d5d8d9d834D8AaD4bB6e418E489?chain=eth&limit=100

**Response:** A JSON object containing the balances of all tokens in the wallet. Each key is a token symbol and the corresponding value is the balance of that token.

### 2. Ethplorer API Balance Fetch

No whitelist used for this approach, returns all tokens that have non-zero balance for a given wallet address. `!Note: may return scam tokens as well` 

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**Endpoint:** /api/balance/{wallet}

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**Method:** GET

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**Description:** This endpoint returns the balance of a given Ethereum wallet by fetching data from the Ethplorer API.

#### Parameters:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**wallet:** The Ethereum wallet address.

**Request:** GET /api/balance/0x40B38765696e3d5d8d9d834D8AaD4bB6e418E489

**Response:** A JSON object containing the balances of all tokens in the wallet. Each key is a token symbol and the corresponding value is the balance of that token.


#### Response example:

    {
        "$Lgc": 30027759.615466926,
        "0GAS": 634693783629.8918,
        "AAVE": 0.25,
        "ABC-RAQ": 0.12345678,
        "AEVO": 36000000.0,
        "AIBEN": 16296830.070638577,
        "AIMEME": 180245928.89033905,
        "ALCOH": 430309801.1317416,
        "ALF": 1000000.0,
        "BABY": 114950644.0196546,
        "BABYKISHU": 1978.02,
        "BABYPOO": 2070442.7303935334,
        "BABYPSYOP": 9282362.362215867,
        "BABYSAMO": 42340.62712453486,
        "BABYSHIB": 19184014452758.484,
        "BALM": 215350255.0224826,
        "BARRETT": 485608427.1148974,
        "BENBABY": 140013081.94892895
    }
