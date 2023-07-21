from brownie import network, AdvancedCollectible
from scripts.helpful_scripts import get_sky, get_account, OPENSEA_URL

sky_metadata_dict = {
    "CRESCENT": "",
    "NEBULA": "https://ipfs.io/ipfs/Qmesajp9Jt2TPXhR7w2wVoMUUzfRQxwWXs4KJ4o7Dh9Dea?filename=0-NEBULA.json",
    "STARS": "https://ipfs.io/ipfs/QmYt6FRy3FZKsMXXvYvrEp8Db3iyApT2U9LPXemiyEZkPN?filename=1-STARS.json",
}


def main():
    print(f"Working on {network.show_active()}")
    advanced_collectible = AdvancedCollectible[-1]
    number_of_collectibles = advanced_collectible.tokenCounter()
    print(f"You have {number_of_collectibles} nfts")
    for token_id in range(number_of_collectibles):
        sky = get_sky(advanced_collectible.tokenIDtoSky(token_id))
        if not advanced_collectible.tokenURI(token_id).startswith("https://"):
            print(f"Setting token URI of {token_id}")
            set_tokenURI(token_id, advanced_collectible, sky_metadata_dict[sky])


def set_tokenURI(token_id, nft_contract, tokenURI):
    account = get_account()
    tx = nft_contract.setTokenURI(token_id, tokenURI, {"from": account})
    tx.wait(1)
    print(
        f"Awesome! You can view your NFT at {OPENSEA_URL.format(nft_contract.address, token_id)}"
    )
    print(f"Your Token URI is: {nft_contract.tokenURI(token_id)}")
    print("Please wait 20 minutes and hit the refresh metadata button")
