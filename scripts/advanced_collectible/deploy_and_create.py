from scripts.helpful_scripts import (
    get_account,
    OPENSEA_URL,
    get_contract,
    fund_with_link,
)
from brownie import AdvancedCollectible, network, config

sample_token_uri = "https://ipfs.io/ipfs/Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json"


def deploy_and_create():
    account = get_account()

    advanced_collectible = AdvancedCollectible.deploy(
        get_contract("vrf_wrapper").address,
        get_contract("link_token").address,
        config["networks"][network.show_active()]["callbackGasLimit"],
        config["networks"][network.show_active()]["requestConfirmations"],
        config["networks"][network.show_active()]["numWords"],
        {"from": account},
    )
    fund_with_link(advanced_collectible.address)
    creating_tx = advanced_collectible.createCollectible({"from": account})
    creating_tx.wait(1)
    print("New token/NFT has been created")

    return advanced_collectible, creating_tx


def main():
    deploy_and_create()
