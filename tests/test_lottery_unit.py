
from brownie import Lottery, accounts, config, network, exceptions
import brownie
from scripts.deploy_lottery import deploy_lottery
from scripts.helpful_script import (
    LOCAL_BLOCKCHAIN_ENVIROMENTS,
    fund_with_link, 
    get_account,
    get_contract
)
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

def test_can_start_and_enter_lottery():
    # Arrange (zorganizowac)
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIROMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    # Act (dzialac)
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    # Assert (dowiesc czegos)
    assert lottery.players(0) == account

def test_can_end_lottery():
    # Arrange (zorganizowac)
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIROMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    fund_with_link(lottery)
    lottery.endLottery({"from": account})
    assert lottery.lottery_state() == 2

def test_pick_winner_corretly():
    # Arrange (zorganizowac)
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIROMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    # start lottery by admin
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    # add another lottery participants
    lottery.enter({"from": get_account(index=1), "value": lottery.getEntranceFee()})
    lottery.enter({"from": get_account(index=2), "value": lottery.getEntranceFee()})
    fund_with_link(lottery)
    transaction = lottery.endLottery({"from": account})
    # mocking responses from chainlink to get random number
    requestId = transaction.events["RequestedRandomness"]["requestId"]
    STATIC_RNG = 777
    get_contract("vrf_coordinator").callBackWithRandomness(
        requestId, 
        STATIC_RNG, 
        lottery.address,
        {"from": account}
    )
    starting_balance_of_account = account.balance()
    balance_of_lottery = lottery.balance()
    # 777 % 3 = 0 
    assert lottery.recentWinner() == account
    assert lottery.balance() == 0
    assert (starting_balance_of_account + balance_of_lottery) == account.balance()