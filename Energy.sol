// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title Decentralized Renewable Energy Trading Smart Contract
/// @author ChatGPT
/// @notice Handles buying/selling of energy units as tokens between producers and consumers.

contract EnergyTrading {
    address public owner;
    uint public tokenPrice = 1 ether; // 1 energy token = 1 ETH by default

    struct User {
        bool isProducer;
        bool isRegistered;
        uint energyBalance; // in energy units
    }

    struct Trade {
        address seller;
        address buyer;
        uint amount;
        uint pricePerUnit;
        uint timestamp;
    }

    mapping(address => User) public users;
    Trade[] public trades;

    event UserRegistered(address indexed user, bool isProducer);
    event EnergyMinted(address indexed producer, uint amount);
    event EnergyPurchased(address indexed buyer, address indexed seller, uint amount, uint pricePerUnit);

    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can call this");
        _;
    }

    modifier onlyProducer() {
        require(users[msg.sender].isProducer, "Only producers can call this");
        _;
    }

    modifier onlyRegistered() {
        require(users[msg.sender].isRegistered, "User not registered");
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    function registerUser(bool isProducer) external {
        require(!users[msg.sender].isRegistered, "User already registered");
        users[msg.sender] = User(isProducer, true, 0);
        emit UserRegistered(msg.sender, isProducer);
    }

    function mintEnergy(uint amount) external onlyProducer onlyRegistered {
        users[msg.sender].energyBalance += amount;
        emit EnergyMinted(msg.sender, amount);
    }

    function buyEnergy(address from, uint amount) external payable onlyRegistered {
        User storage seller = users[from];
        User storage buyer = users[msg.sender];

        require(seller.isProducer, "Seller must be producer");
        require(seller.energyBalance >= amount, "Insufficient energy");
        require(msg.value >= amount * tokenPrice, "Not enough ETH sent");

        seller.energyBalance -= amount;
        buyer.energyBalance += amount;

        // Pay the producer
        payable(from).transfer(msg.value);

        // Log the trade
        trades.push(Trade({
            seller: from,
            buyer: msg.sender,
            amount: amount,
            pricePerUnit: tokenPrice,
            timestamp: block.timestamp
        }));

        emit EnergyPurchased(msg.sender, from, amount, tokenPrice);
    }

    function getMyBalance() external view onlyRegistered returns (uint) {
        return users[msg.sender].energyBalance;
    }

    function getTradeHistory() external view returns (Trade[] memory) {
        return trades;
    }

    function setTokenPrice(uint newPrice) external onlyOwner {
        tokenPrice = newPrice;
    }

    function getUserInfo(address user) external view returns (bool isProducer, bool isRegistered, uint balance) {
        User memory u = users[user];
        return (u.isProducer, u.isRegistered, u.energyBalance);
    }

    function withdraw() external onlyOwner {
        payable(owner).transfer(address(this).balance);
    }
}
