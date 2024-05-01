# Token Checker
Mini app fetching token balances for a given wallet address. 
Currently supports only ETH chain. 

## Features
Wallet Balance Retrieval: The application offers two endpoints for obtaining the balance of a specified Ethereum wallet. The first endpoint retrieves the balance through direct contract calls to the Ethereum network, while the second endpoint utilizes the Ethplorer API for balance retrieval.

## Environment Variables
The application uses the following environment variables:

**INFURA_API_KEY:** Your Infura API key. This is used to connect to the Ethereum network.

**ETHPLORER_API_KEY:** Your Ethplorer API key. This is used to fetch data from the Ethplorer API.

**MORALIS_API_KEY:** Your Moralis API key. This is used to fetch top 100 Ethereum chain tokens by market cap.

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
    pip install moralis

## Usage
To start the application, run the following command:

    py checker.py


## API Documentation

This Python script provides two API endpoints for fetching Ethereum wallet balances.

### 1. Direct Balance Fetch

Uses Moralis API to get a list of top 100 tokens by market cap on Ethereum. Resource: [docs.moralis.io](https://docs.moralis.io/market-insights-api/reference/get-top-erc20-tokens-by-market-cap)

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**Endpoint:** /direct/balance/{wallet}

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**Method:** GET

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**Description:** This endpoint returns the balance of a given Ethereum wallet by making direct contract calls to the Ethereum network.

#### Parameters:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**wallet:** The Ethereum wallet address.

#### Query Parameters:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**chain:** The blockchain network to use. Defaults to 'eth'. `!Note: currently only Ethereum is supported` 

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**limit:** The maximum number of tokens to fetch. Must be an integer between 1 and 100. Defaults to 10.

**Request:** GET /direct/balance/0x40B38765696e3d5d8d9d834D8AaD4bB6e418E489?chain=eth&limit=100

**Response:** A JSON object containing the balances of all tokens in the wallet and the total value in USD.

### 2. Ethplorer API Balance Fetch

No whitelist used for this approach, returns all tokens that have non-zero balance for a given wallet address. `!Note: may return scam tokens as well` 

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**Endpoint:** /api/balance/{wallet}

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**Method:** GET

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**Description:** This endpoint returns the balance of a given Ethereum wallet by fetching data from the Ethplorer API.

#### Parameters:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**wallet:** The Ethereum wallet address.

**Request:** GET /api/balance/0x40B38765696e3d5d8d9d834D8AaD4bB6e418E489

**Response:** A JSON object containing the balances of all tokens in the wallet and the total value in USD.

#### Response example:

    {
        "balances": {
            "AAVE": 0.25,
            "BGBG": 1023.805463897978,
            "BONE": 88.88888888000001,
            "COMP": 1.026166,
            "DONG": 6.9,
            "ETH": 1443694.7955230272,
            "ICG": 258.0,
            "INNBC": 50000000000.0,
            "JAM": 1111.0,
            "LINK": 2400001.213955,
            "LOOT": 69.0,
            "PEPE": 2000000.0,
            "PEPE2.0": 74257844.0,
            "POOH": 19604190.95335947,
            "SHIB": 31753251930362.97,
            "SHIBDOGE": 1.454384246410173e+18,
            "TEST": 1000.0,
            "TREAT": 33334.0,
            "TSUKA": 5.55,
            "UNI": 2.403724,
            "USDC": 10.0,
            "VIRAL": 1.0,
            "WOJAK2.69": 266.333662948,
            "XEN": 313494.0,
            "ZUM": 1350000.0
        },
        "total_value": 4884777592.40959
    }   

### 3. Moralis top 100 tokens fetch

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**Endpoint:** /moralis

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**Method:** GET

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**Description:** This endpoint returns a list of the top 100 ERC20 tokens by market capitalization. The data is fetched from the Moralis API.

#### Parameters:

None

**Response:** A JSON array containing the top 100 ERC20 tokens by market capitalization. Each element in the array is a JSON object representing a token.

#### Response example:

    [
        {
            "contract_address": "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
            "market_cap_usd": "351277420619",
            "price_24h_percent_change": "-2.93582",
            "price_7d_percent_change": "-9.08268853870393",
            "price_usd": "2881.58",
            "token_decimals": "18",
            "token_logo": "https://market-data-images.s3.us-east-1.amazonaws.com/tokenImages/0xf3052f6ed37615d0739e5341097668a189b40574ff102fc5509909ba305351b7.png",
            "token_name": "Wrapped Ether",
            "token_symbol": "WETH"
        },
        {
            "contract_address": "0xdac17f958d2ee523a2206206994597c13d831ec7",
            "market_cap_usd": "110246059722",
            "price_24h_percent_change": "0.28852",
            "price_7d_percent_change": "-0.01794364794398013",
            "price_usd": "0.999689",
            "token_decimals": "6",
            "token_logo": "https://market-data-images.s3.us-east-1.amazonaws.com/tokenImages/0x63adcb79842ad73769d6f2350d9cab2c8b8e0d37f6071dee9418cbd53319543d.png",
            "token_name": "Tether USD",
            "token_symbol": "USDT"
        },
        {
            "contract_address": "0xb8c77482e45f1f44de1745f52c74426c631bdd52",
            "market_cap_usd": "83552054276",
            "price_24h_percent_change": "-2.17573",
            "price_7d_percent_change": "-8.94350968279868",
            "price_usd": "545.37",
            "token_decimals": "18",
            "token_logo": "https://market-data-images.s3.us-east-1.amazonaws.com/tokenImages/0x6b1fc7eb8799dc72fe25ec4ef2518ccb23ca822dddb4978106d378d915509970.png",
            "token_name": "BNB",
            "token_symbol": "BNB"
        },
        ...
    ]


