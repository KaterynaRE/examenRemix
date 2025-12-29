from web3 import Web3
import json

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

account = w3.eth.accounts[0]
private_key = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"

DEPOSIT_BANK_ADDRESS = w3.to_checksum_address("0xe7f1725E7734CE288F8367e1Bb143E90bb3F0512")
INTEREST_CALCULATOR_ADDRESS = w3.to_checksum_address("0x5FbDB2315678afecb367f032d93F642f64180aa3")

with open("DepositBankABI.json") as f:
    deposit_abi = json.load(f)

with open("InterestCalculatorABI.json") as f:
    interest_abi = json.load(f)

deposit_bank = w3.eth.contract(address=DEPOSIT_BANK_ADDRESS, abi=deposit_abi)
interest_calculator = w3.eth.contract(address=INTEREST_CALCULATOR_ADDRESS, abi=interest_abi)

nonce = w3.eth.get_transaction_count(account)
tx = interest_calculator.functions.setBank(DEPOSIT_BANK_ADDRESS).build_transaction({
    'from': account,
    'gas': 100000,
    'nonce': nonce
})
signed_tx = w3.eth.account.sign_transaction(tx, private_key=private_key)
tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
w3.eth.wait_for_transaction_receipt(tx_hash)


def deposit(amount_eth):
    nonce = w3.eth.get_transaction_count(account)
    tx = deposit_bank.functions.deposit().build_transaction({
        'from': account,
        'value': w3.to_wei(amount_eth, 'ether'),
        'gas': 2000000,
        'nonce': nonce,
    })
    signed_tx = w3.eth.account.sign_transaction(tx, private_key=private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    print(f"Deposit sent: {tx_hash.hex()}")
    w3.eth.wait_for_transaction_receipt(tx_hash)
    print("Deposit confirmed!\n")

def accrue_interest():
    print("Interest is automatically accrued on deposit by the contract.\n")

def get_balance():
    balance = deposit_bank.functions.balances(account).call()
    print("Your DepositBank balance:", w3.from_wei(balance, 'ether'), "ETH\n")

def fund_interest_calculator(amount_eth=1):
    balance = w3.eth.get_balance(INTEREST_CALCULATOR_ADDRESS)
    if balance == 0:
        print(f"Funding InterestCalculator with {amount_eth} ETH...")
        tx = {
            'from': account,
            'to': INTEREST_CALCULATOR_ADDRESS,
            'value': w3.to_wei(amount_eth, 'ether'),
            'gas': 200000,
            'gasPrice': w3.to_wei(1, 'gwei'),
            'nonce': w3.eth.get_transaction_count(account)
        }
        signed_tx = w3.eth.account.sign_transaction(tx, private_key=private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        w3.eth.wait_for_transaction_receipt(tx_hash)
        print("InterestCalculator funded!\n")

def get_interest():
    fund_interest_calculator(1)

    nonce = w3.eth.get_transaction_count(account)
    tx = deposit_bank.functions.payInterest().build_transaction({
        'from': account,
        'gas': 300000,
        'nonce': nonce
    })

    signed_tx = w3.eth.account.sign_transaction(tx, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    w3.eth.wait_for_transaction_receipt(tx_hash)
    print("Interest payment confirmed!\n")


def withdraw(amount_eth):
    nonce = w3.eth.get_transaction_count(account)
    tx = deposit_bank.functions.withdraw(
        w3.to_wei(amount_eth, 'ether')
    ).build_transaction({
        'from': account,
        'gas': 2000000,
        'nonce': nonce,
    })
    signed_tx = w3.eth.account.sign_transaction(tx, private_key=private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    w3.eth.wait_for_transaction_receipt(tx_hash)
    print("Withdrawal confirmed!\n")

while True:
    print("1: Deposit\n2: Check Balance\n3: Accrue Interest\n4: Get Interest\n5: Withdraw\n0: Exit")
    choice = input("Choose an action: ")

    if choice == "1":
        amount = float(input("Amount in ETH: "))
        deposit(amount)
    elif choice == "2":
        get_balance()
    elif choice == "3":
        accrue_interest()
    elif choice == "4":
        get_interest()
    elif choice == "5":
        amount = float(input("Withdraw ETH: "))
        withdraw(amount)
    elif choice == "0":
        break
    else:
        print("Invalid option\n")