from web3 import Web3
import json

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

account = w3.eth.accounts[0]
private_key = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"

DEPOSIT_BANK_ADDRESS = w3.to_checksum_address("0xe7f1725e7734ce288f8367e1bb143e90bb3f0512")
INTEREST_CALCULATOR_ADDRESS = w3.to_checksum_address("0x5fbdb2315678afecb367f032d93f642f64180aa3")

with open("DepositBankABI.json") as f:
    deposit_abi = json.load(f)

with open("InterestCalculatorABI.json") as f:
    interest_abi = json.load(f)

deposit_bank = w3.eth.contract(address=DEPOSIT_BANK_ADDRESS, abi=deposit_abi)
interest_calculator = w3.eth.contract(address=INTEREST_CALCULATOR_ADDRESS, abi=interest_abi)

nonce = w3.eth.get_transaction_count(account)
tx = deposit_bank.functions.setCalculator(INTEREST_CALCULATOR_ADDRESS).build_transaction({
    'from': account,
    'gas': 200000,
    'nonce': nonce
})
signed_tx = w3.eth.account.sign_transaction(tx, private_key=private_key)
tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
print("Calculator set:", tx_hash.hex())
w3.eth.wait_for_transaction_receipt(tx_hash)
print("Calculator is ready!\n")

def deposit(amount_eth):
    nonce = w3.eth.get_transaction_count(account)
    tx = deposit_bank.functions.deposit().build_transaction({
        'from': account,
        'value': w3.to_wei(amount_eth, 'ether'),
        'gas': 2000000,
        'nonce': nonce
    })
    signed_tx = w3.eth.account.sign_transaction(tx, private_key=private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    print(f"Deposit sent: {tx_hash.hex()}")
    w3.eth.wait_for_transaction_receipt(tx_hash)
    print("Deposit confirmed!")

def get_balance():
    balance = deposit_bank.functions.getUserBalance(account).call()
    print("Your DepositBank balance:", w3.from_wei(balance, 'ether'), "ETH")

def accrue_interest():
    nonce = w3.eth.get_transaction_count(account)
    tx = interest_calculator.functions.accrueInterest(account).build_transaction({
        'from': account,
        'gas': 2000000,
        'nonce': nonce
    })
    signed_tx = w3.eth.account.sign_transaction(tx, private_key=private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    print(f"Interest accrued: {tx_hash.hex()}")
    w3.eth.wait_for_transaction_receipt(tx_hash)
    print("Interest accrual confirmed!")

def pay_interest():
    nonce = w3.eth.get_transaction_count(account)
    tx = interest_calculator.functions.payInterest(account).build_transaction({
        'from': account,
        'gas': 2000000,
        'nonce': nonce
    })
    signed_tx = w3.eth.account.sign_transaction(tx, private_key=private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    print(f"Interest paid: {tx_hash.hex()}")
    w3.eth.wait_for_transaction_receipt(tx_hash)
    print("Interest payment confirmed!")

def withdraw(amount_eth):
    nonce = w3.eth.get_transaction_count(account)
    tx = deposit_bank.functions.withdraw(
        w3.to_wei(amount_eth, 'ether')
    ).build_transaction({
        'from': account,
        'gas': 2000000,
        'nonce': nonce
    })
    signed_tx = w3.eth.account.sign_transaction(tx, private_key=private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    print("Withdraw tx:", tx_hash.hex())
    w3.eth.wait_for_transaction_receipt(tx_hash)
    print("Withdrawal confirmed!")

while True:
    print("\n1: Deposit\n2: Check Balance\n3: Accrue Interest\n4: Get Interest\n5: Withdraw\n0: Exit")
    choice = input("Choose an action: ")

    if choice == "1":
        amount = float(input("Amount in ETH: "))
        deposit(amount)
    elif choice == "2":
        get_balance()
    elif choice == "3":
        accrue_interest()
    elif choice == "4":
        pay_interest()
    elif choice == "5":
        amount = float(input("Withdraw ETH: "))
        withdraw(amount)    
    elif choice == "0":
        break
    else:
        print("Invalid option")
