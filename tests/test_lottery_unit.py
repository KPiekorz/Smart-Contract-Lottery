
from brownie import Lottery, accounts, config, network
from web3 import Web3
from scripts.deploy_lottery import deploy_lottery

def test_get_entrance_fee():
    lottery = deploy_lottery()
    entrence_fee = lottery.getEntranceFee()
