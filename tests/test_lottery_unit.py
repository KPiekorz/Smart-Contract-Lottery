
from brownie import Lottery, accounts, config, network, exceptions
import brownie
from scripts.deploy_lottery import deploy_lottery
from scripts.helpful_script import LOCAL_BLOCKCHAIN_ENVIROMENTS, get_account
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

def test_cant_enter_unless_started():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIROMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    # Act / assert
    print(f"Account: {get_account()}")
    with pytest.raises(exceptions.VirtualMachineError):
        lottery.enter({"from": get_account(), "value": lottery.getEntranceFee()})