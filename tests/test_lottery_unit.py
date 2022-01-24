
from brownie import Lottery, accounts, config, network
from web3 import Web3
from scripts.deploy_lottery import deploy_lottery

def test_get_entrance_fee():
    account = accounts[0]
    lottery = Lottery.deploy(
        config["networks"][network.show_active()]["eth_usd_price_feed"],
        {"from": account}
    )
    print(Web3.toWei(0.015, "ether"))
    print(Web3.toWei(0.025, "ether"))
    print(lottery.getEntranceFee())
    assert lottery.getEntranceFee() > Web3.toWei(0.015, "ether")
    assert lottery.getEntranceFee() < Web3.toWei(0.025, "ether")
