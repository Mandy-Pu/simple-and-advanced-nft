from brownie import AdvancedCollectible, accounts
from scripts.helpful_scripts import get_account, fund_with_link


def main():
    account = get_account()
    advanced_collectible = AdvancedCollectible[-1]
    fund_with_link(advanced_collectible.address)
    creation_tx = advanced_collectible.createCollectible({"from": account})
    creation_tx.wait(1)
    print("Collectible Created!")
