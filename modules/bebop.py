#!/usr/bin/env python3
import os, sys, time, random
from dotenv import load_dotenv
from web3 import Web3
from eth_account import Account
from colorama import init, Fore, Style

init(autoreset=True)
load_dotenv()

def display_header():
    print(Style.BRIGHT + Fore.CYAN + "======================================")
    print(Style.BRIGHT + Fore.CYAN + "            Bebop Bot                 ")
    print(Style.BRIGHT + Fore.CYAN + "====================================\n")

display_header()

RPC_URL = "https://carrot.megaeth.com/rpc"
EXPLORER_URL = "https://megaexplorer.xyz/"
w3 = Web3(Web3.HTTPProvider(RPC_URL))
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
if not PRIVATE_KEY:
    raise Exception("No PRIVATE_KEY in .env")
account = Account.from_key(PRIVATE_KEY)
WETH_CONTRACT = Web3.to_checksum_address("0x4eB2Bd7beE16F38B1F4a0A5796Fffd028b6040e9")

# ABI untuk fungsi deposit dan withdraw
contract_abi = [
     {
    "inputs": [],
    "name": "deposit",
    "outputs": [],
    "stateMutability": "payable",
    "type": "function"
  },
  {
    "inputs": [
      { "internalType": "uint256", "name": "wad", "type": "uint256" }
    ],
    "name": "withdraw",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  }
]
contract = w3.eth.contract(address=WETH_CONTRACT, abi=contract_abi)

def get_random_amount():
    min_val = 0.00001
    max_val = 0.00002
    amount = random.uniform(min_val, max_val)
    amount = float(f"{amount:.4f}")
    return w3.to_wei(amount, "ether")

def get_random_delay():
    return random.randint(1 * 60 * 1000, 3 * 60 * 1000)

def wrap_mon(amount):
    try:
        print(Fore.BLUE + "🪫 Starting Bebop ⏩⏩⏩⏩")
        print(Fore.MAGENTA + f"🔄 Wrapping {w3.from_wei(amount, 'ether')} ETH to WETH")
        nonce = w3.eth.get_transaction_count(account.address)
        tx = contract.functions.deposit().build_transaction({
            'from': account.address,
            'value': amount,
            'gas': 210000,
            'nonce': nonce,
            'gasPrice': w3.eth.gas_price
        })
        signed_tx = account.sign_transaction(tx)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        print(Fore.GREEN + "✅ Successfully wrapped ETH to WETH")
        print(Fore.LIGHTBLACK_EX + f"➡️  Hash: {tx_hash.hex()}")
        # Mengganti waitForTransactionReceipt dengan wait_for_transaction_receipt
        w3.eth.wait_for_transaction_receipt(tx_hash)
    except Exception as e:
        print(Fore.RED + f"❌ Error while wrapping ETH to WETH: {str(e)}")

def unwrap_mon(amount):
    try:
        print(Fore.MAGENTA + f"🔄 Unwrapping {w3.from_wei(amount, 'ether')} WETH to ETH")
        nonce = w3.eth.get_transaction_count(account.address)
        tx = contract.functions.withdraw(amount).build_transaction({
            'from': account.address,
            'gas': 210000,
            'nonce': nonce,
            'gasPrice': w3.eth.gas_price
        })
        signed_tx = account.sign_transaction(tx)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        print(Fore.GREEN + "✅ Successfully unwrapped WETH to ETH")
        print(Fore.LIGHTBLACK_EX + f"➡️  Hash: {tx_hash.hex()}")
        # Mengganti waitForTransactionReceipt dengan wait_for_transaction_receipt
        w3.eth.wait_for_transaction_receipt(tx_hash)
    except Exception as e:
        print(Fore.RED + f"❌ Error while unwrapping WMON to MON: {str(e)}")

def run_swap_cycle(cycles=1):
    try:
        for i in range(cycles):
            random_amount = get_random_amount()
            random_delay = get_random_delay()
            wrap_mon(random_amount)
            unwrap_mon(random_amount)
            if i < cycles - 1:
                wait_minutes = random_delay / 1000 / 60
                print(Fore.LIGHTBLACK_EX + f"⏳ Waiting for {wait_minutes} minutes")
                time.sleep(random_delay / 1000)
        print(Fore.GREEN + "✅ Finished")
    except Exception as e:
        print(Fore.RED + f"❌ Error during swap cycle: {str(e)}")

if __name__ == '__main__':
    try:
        run_swap_cycle(1)
    except Exception as e:
        print(Fore.RED + f"❌ Error in runSwapCycle: {str(e)}")
