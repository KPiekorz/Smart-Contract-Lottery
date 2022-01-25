from brownie import (
    accounts,
    network
)
from scripts.deploy_lottery import (
    deploy_lottery,
    start_lotery,
    enter_lottery,
    end_lottery,

)
from scripts.helpful_script import (
    LOCAL_BLOCKCHAIN_ENVIROMENTS,
    fund_with_link, 
    get_account,
    get_contract
)
import pytest
import time

def test_can_pick_winner():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIROMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    fund_with_link(lottery)
    lottery.endLottery({"from": account})
    time.sleep(60)
    assert lottery.recentWinner() == account
    assert lottery.balance == 0