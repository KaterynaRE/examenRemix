// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract InterestCalculator {
    address public bank;
    uint256 public interestRate; 

    mapping(address => uint256) public interestAccrued;

    modifier onlyBank() {
        require(msg.sender == bank, "Only bank");
        _;
    }

    constructor(uint256 _rate) {
        interestRate = _rate;
    }

    function setBank(address _bank) external {
        bank = _bank;
    }

    function accrueInterest(address user, uint256 balance) external onlyBank {
        uint256 interest = (balance * interestRate) / 100;
        interestAccrued[user] += interest;
    }

    function payInterest(address user) external onlyBank {
        uint256 amount = interestAccrued[user];
        require(amount > 0, "No interest");
        interestAccrued[user] = 0;
        payable(user).transfer(amount);
    }

    receive() external payable {}
}


