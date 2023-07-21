from brownie import (
    accounts,
    network,
    config,
    Contract,
    LinkToken,
    VRFCoordinatorV2Mock,
    VRFV2Wrapper,
    MockV3Aggregator,
)

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]
OPENSEA_URL = "https://testnets.opensea.io/assets/sepolia/{}/{}"
_BASEFEE = 100000000000000000
_GASPRICELINK = 1000000000
_DECIMALS = 18
_INITIALANSWER = 3000000000000000
SKY_MAPPING = {0: "CRESCENT", 1: "NEBULA", 2: "STARS"}


def get_sky(sky_number):
    return SKY_MAPPING[sky_number]


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]

    return accounts.add(config["wallets"]["from_key"])


contract_to_mock = {
    "vrf_wrapper": VRFV2Wrapper,
    "link_token": LinkToken,
    "vrf_coordinator": VRFCoordinatorV2Mock,
}


def get_contract(contract_name):
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <= 0:
            deploy_mocks()
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )
    return contract


def deploy_mocks():
    """
    Use this script if you want to deploy mocks to a testnet
    """
    print(f"The active network is {network.show_active()}")
    print("Deploying mocks...")
    account = get_account()
    print("Deploying Mock LinkToken...")
    link_token = LinkToken.deploy({"from": account})
    print(f"Link Token deployed to {link_token.address}")
    print("Deploying Mock VRF Coordinator...")
    vrf_coordinator = VRFCoordinatorV2Mock.deploy(
        _BASEFEE, _GASPRICELINK, {"from": account}
    )
    print(f"VRFCoordinator deployed to {vrf_coordinator.address}")
    print("Deploying Mock V3 Aggregator...")
    v3_aggregtor = MockV3Aggregator.deploy(_DECIMALS, _INITIALANSWER, {"from": account})
    print(f"V3Aggregator deployed to {v3_aggregtor.address}")
    print("Deploying Mock VRF Wrapper...")
    vrf_wrapper = VRFV2Wrapper.deploy(
        link_token.address,
        v3_aggregtor.address,
        vrf_coordinator.address,
        {"from": account},
    )
    print(f"VRF Wrapper deployed to {vrf_wrapper.address}")
    print("Configuring the VRF Wrapper...")
    vrf_wrapper.setConfig(
        60000,
        52000,
        10,
        0xD89B2BF150E3B9E13446986E571FB9CAB24B13CEA0A43EA20A6049A85CC807CC,
        10,
        {"from": account},
    )
    print("Funding the VRF Wrapper Subscription...")
    vrf_coordinator.fundSubscription(1, 10000000000000000000, {"from": account})
    print("All done!")


def fund_with_link(
    contract_address,
    account=None,
    link_token=None,
    amount=10000000000000000000,
):
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link_token")
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        amount = config["networks"]["sepolia"]["fee"]
    tx = link_token.transfer(contract_address, amount, {"from": account})
    tx.wait(1)
    print("Contract funded with LINK token")
    return tx
