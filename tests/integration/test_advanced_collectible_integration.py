from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_account,
    get_contract,
    fund_with_link,
)
from scripts.advanced_collectible.deploy_and_create import deploy_and_create
from brownie import network, AdvancedCollectible, config
import pytest, time


def test_can_create_advanced_collectible_integration():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for integration testing")

    account = get_account()
    # advanced_collectible, creation_tx = deploy_and_create()
    advanced_collectible = AdvancedCollectible[-1]
    fund_with_link(advanced_collectible.address)
    creating_tx = advanced_collectible.createCollectible({"from": account})
    creating_tx.wait(1)
    print("New token/NFT has been created")
    time.sleep(60)
    # random = randomness_tx.events["skyAssigned"]["newTokenID"]

    assert advanced_collectible.tokenCounter() == 2
