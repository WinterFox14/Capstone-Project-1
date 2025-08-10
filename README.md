# EnergyTrading Smart Contract (Energy.sol)

## Overview 
The **EnergyTrading ** smart contract is designed for decentralized renewable energy trading between producers and consumers.  
It allows producers to mint energy tokens and consumers to purchase them securely on the blockchain.

---

## Functions

- **`registerUser(bool isProducer)`**
  - Registers a new user as either a **Producer** (can mint and sell energy) or **Consumer** (can buy energy).
  - Can only be called once per wallet address.

- **`mintEnergy(uint amount)`**
  - Allows a registered producer to create (mint) new energy tokens.
  - Increases the producer's energy balance.

- **`buyEnergy(address seller, uint amount)`**
  - Enables a registered consumer to purchase energy tokens from a producer.
  - Transfers ETH to the seller based on the set `tokenPrice`.
  - Updates the energy balances for both buyer and seller.

- **`setTokenPrice(uint newPrice)`**
  - Allows only the **Owner** of the contract to change the price of each energy token.
  - Price is set in **wei** (1 ether = 1e18 wei).

- **`getTradeHistory()`**
  - Returns a list of all previous trades.
  - Each trade record contains:
    - Seller address
    - Buyer address
    - Amount of energy traded
    - Price per unit
    - Timestamp of the trade

---

## Modifiers

- **`onlyOwner`**
  - Restricts access to functions so only the contract owner can call them.

- **`onlyProducer`**
  - Restricts access to functions so only registered producers can call them.

- **`onlyRegistered`**
  - Restricts access to functions so only registered users (producers or consumers) can call them.

---

## Events

- **`UserRegistered(address user, bool isProducer)`**
  - Emitted when a new user is registered.

- **`EnergyMinted(address producer, uint amount)`**
  - Emitted when a producer mints new energy.

- **`EnergyPurchased(address buyer, address seller, uint amount, uint pricePerUnit)`**
  - Emitted when a consumer buys energy from a producer.

---

## Deployment
1. Open the contract in [Remix IDE](https://remix.ethereum.org/).
2. Compile with **Solidity version 0.8.20**.
3. Deploy to a local blockchain, testnet, or mainnet.
4. Interact with the functions via Remix, web3.js, or ethers.js.

---

## License
This project is licensed under the MIT License.
