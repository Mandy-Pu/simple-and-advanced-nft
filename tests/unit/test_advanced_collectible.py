from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_account,
    get_contract,
)
from scripts.advanced_collectible.deploy_and_create import deploy_and_create
from brownie import network, AdvancedCollectible, config
import pytest


def test_can_create_advanced_collectible():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")

    advanced_collectible, creation_tx = deploy_and_create()
    requestID = creation_tx.events["requestedCollectible"]["requestID"]

    vrf_coordinator = get_contract("vrf_coordinator")
    print(f"VRF Coordinator address: {vrf_coordinator}")
    vrf_wrapper = get_contract("vrf_wrapper")
    print(f"VRF Wrapper address: {vrf_wrapper}")

    randomness_tx = vrf_coordinator.fulfillRandomWords(
        requestID, vrf_wrapper.address, {"from": get_account()}
    )
    randomness_tx.wait(1)
    # random = randomness_tx.events["skyAssigned"]["newTokenID"]

    assert advanced_collectible.tokenCounter() == 1
    assert advanced_collectible.tokenIDtoSky(0) == 2
