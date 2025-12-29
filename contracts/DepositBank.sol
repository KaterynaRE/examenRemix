// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "./InterestCalculator.sol";

contract DepositBank {
    mapping(address => uint256) public balances;
    InterestCalculator public calculator;

    constructor(address _calculator) {
        calculator = InterestCalculator(payable(_calculator));
    }

    function deposit() external payable {
        require(msg.value > 0, "Zero deposit");

        balances[msg.sender] += msg.value;
        calculator.accrueInterest(msg.sender, balances[msg.sender]);
    }

    function withdraw(uint256 amount) external {
        require(balances[msg.sender] >= amount, "Not enough");

        balances[msg.sender] -= amount;
        payable(msg.sender).transfer(amount);
    }

    function payInterest() external {
        calculator.payInterest(msg.sender);
    }

    receive() external payable {}
}