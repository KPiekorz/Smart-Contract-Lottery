
from brownie import Lottery, accounts, config, network
from scripts.deploy_lottery import deploy_lottery
from scripts.helpful_script import LOCAL_BLOCKCHAIN_ENVIROMENTS
from web3 import Web3
import pytest

def test_get_entrance_fee():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIROMENTS:
        pytest.skip()
    # Arrange
    lottery = deploy_lottery()
    # Act
    # 2,000
    expected_entrance_fee = Web3.toWei(0.025, "ether")
    entrence_fee = lottery.getEntranceFee()
    # Assert
    print(f"Entrance fee {entrence_fee} and expected {expected_entrance_fee}")
    assert expected_entrance_fee == entrence_fee
