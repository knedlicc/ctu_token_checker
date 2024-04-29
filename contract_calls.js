const express = require('express');
const { Web3 } = require('web3');
require('dotenv').config();

const app = express();
app.use(express.json());

const INFURA_API_KEY = process.env.INFURA_API_KEY;
const web3 = new Web3('https://mainnet.infura.io/v3/' + INFURA_API_KEY);

const ERC20_ABI = [
    // balanceOf
    {
        "constant": true,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "type": "function"
    },
    // decimals
    {
        "constant": true,
        "inputs": [],
        "name": "decimals",
        "outputs": [{"name": "", "type": "uint8"}],
        "type": "function"
    },
    // symbol
    {
        "constant": true,
        "inputs": [],
        "name": "symbol",
        "outputs": [{"name": "", "type": "string"}],
        "type": "function"
    }
];


const whitelist = [
    '0xdAC17F958D2ee523a2206206994597C13D831ec7', // USDT
    '0x6B175474E89094C44Da98b954EedeAC495271d0F', // DAI
    '0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599', // WBTC
    '0x514910771AF9Ca656af840dff83E8264EcF986CA', // LINK
    '0x0bc529c00C6401aEF6D220BE8C6Ea1667F6Ad93e', // YFI
    '0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984', // UNI
    '0x7Fc66500c84A76Ad7e9c93437bFc5Ac33E2DDaE9', // AAVE
    '0x0d8775f648430679A709E98d2b0Cb6250d2887EF', // BAT
    '0x0Ae055097C6d159879521C384F1D2123D1f195e6', // KP3R
    '0x0D8775F648430679A709E98d2b0Cb6250d2887EF', // STAKE
    '0x0f5D2fB29fb7d3CFeE444a200298f468908cC942', // MANA
    '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48', // USDC
    '0x50327c6c5a14DCaDE707ABad2E27eB517df87AB5', // TRX
    '0x6f259637dcD74C767781E37Bc6133cd6A68aa161', // HT
    '0x6b3595068778dd592e39a122f4f5a5cf09c90fe2', // SUSHI
    '0x0E29e5AbbB5FD88e28b2d355774e73BD47dE3bcd', // HAKKA
    '0x8E870D67F660D95d5be530380D0eC0bd388289E1', // USDP
    '0x0f7F961648aE6Db43C75663aC7E5414Eb79b5704', // XIO
    '0x4E15361FD6b4BB609Fa63C81A2be19d873717870', // FTM
    '0x1f573d6fb3f13d689ff844b4ce37794d79a7ff1c', // BNT
    '0x3c3a81e81dc49A522A592e7622A7E711c06bf354', // MNT
];

app.get('/balances', async (req, res) => {
    const wallet = req.query.wallet;
    const balances = {};
    try {
        const ethBalance = await web3.eth.getBalance(wallet);
        balances['ETH'] = Number(web3.utils.fromWei(ethBalance, 'ether'));
        for (const token of whitelist) {
            const contract = new web3.eth.Contract(ERC20_ABI, token);
            const ticker = await contract.methods.symbol().call();
            const result = await contract.methods.balanceOf(wallet).call();
            const decimals = await contract.methods.decimals().call();
            balances[ticker] = Number(result) / Math.pow(10, parseInt(decimals));
        }

        res.json(balances);
    } catch (err) {
        console.log(err);
        res.status(500).json({ error: 'Error fetching balances' });
    }
});

app.listen(3000, () => console.log('Server running on port 3000'));