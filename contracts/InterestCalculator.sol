// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract InterestCalculator {
    address public owner;

    mapping(address => uint256) public balances;
    mapping(address => uint256) public interestAccrued;

    uint256 public interestRate; 

    event InterestPaid(address indexed user, uint256 amount);

    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner");
        _;
    }

    constructor(uint256 _interestRate) {
        owner = msg.sender;
        interestRate = _interestRate;
    }

    function setBalance(address user, uint256 amount) external {
        balances[user] = amount;
    }

    function accrueInterest(address user) external {
        uint256 interest = (balances[user] * interestRate) / 100;
        interestAccrued[user] += interest;
    }

    function payInterest(address user) external {
        uint256 amount = interestAccrued[user];
        require(amount > 0, "No interest");

        interestAccrued[user] = 0;
        payable(user).transfer(amount);

        emit InterestPaid(user, amount);
    }

    receive() external payable {}
}
