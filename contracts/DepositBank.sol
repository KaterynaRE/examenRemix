// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "./InterestCalculator.sol";

contract DepositBank {
    address public owner;
    uint256 public maxBalance;
    bool public contractActive;
    uint256 public minDeposit;

    InterestCalculator public calculator;

    mapping(address => uint256) public balances;

    event DepositReceived(address indexed from, uint256 amountWei, uint256 amountMicroether);
    event Withdraw(address indexed user, uint256 amount);

    error NotOwner();
    error ContractInactive();

    constructor(
        address _owner,
        uint256 _maxBalance,
        bool _active,
        uint256 _minDeposit
    ) {
        owner = _owner;
        maxBalance = _maxBalance;
        contractActive = _active;
        minDeposit = _minDeposit;
    }

    modifier onlyOwner() {
        if (msg.sender != owner) revert NotOwner();
        _;
    }

    modifier isActive() {
        if (!contractActive) revert ContractInactive();
        _;
    }

    function setCalculator(address _calculator) external onlyOwner {
        calculator = InterestCalculator(payable(_calculator));
    }

    function deposit() external payable isActive {
        require(msg.value >= minDeposit, "Deposit too small");

        balances[msg.sender] += msg.value;

        calculator.setBalance(msg.sender, balances[msg.sender]);
        calculator.accrueInterest(msg.sender);

        uint256 microether = msg.value / 1e12;
        emit DepositReceived(msg.sender, msg.value, microether);
    }

    function withdraw(uint256 amount) external isActive {
        require(balances[msg.sender] >= amount, "Insufficient balance");

        balances[msg.sender] -= amount;

        calculator.setBalance(msg.sender, balances[msg.sender]);

        payable(msg.sender).transfer(amount);
        emit Withdraw(msg.sender, amount);
    }

    function getUserBalance(address user) external view returns (uint256) {
        return balances[user];
    }

    receive() external payable {}
}
