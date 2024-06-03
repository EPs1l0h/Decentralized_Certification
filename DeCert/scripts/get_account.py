from brownie import accounts, DIDRegistry, network
def getAccount(account_name):
    if network.show_active() == "development":
        return accounts[0]
    else:
        return accounts.load(account_name)
