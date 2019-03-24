from web3 import Web3, HTTPProvider, IPCProvider
from os import path
import json
import time


INFURA_URL = 'http://ropsten.infura.io/'

class ContractHandler:
    def __init__(self, contract_address):
        self.web3 = Web3(HTTPProvider("https://ropsten.infura.io/v3/512b45c586ea4b3f9ab564ac910e20f0"))
        self.contract_address = Web3.toChecksumAddress(contract_address)
        v = self.web3.eth.account.privateKeyToAccount('0x3953B6E3DD94D5A5D3B342656EC60F48BB44AFC64E78F7CD50918AD2337B44DE')
        self.web3.eth.account.defaultAccount = v
        dir_path = path.dirname(path.realpath(__file__))
        with open(str(path.join(dir_path, 'contract_abi.json')), 'r') as abi_definition:
            self.abi = json.load(abi_definition)
        self.contract = self.web3.eth.contract(address=self.contract_address, abi=self.abi)

    def handle_event(self, event):
        print(event)

    def log_loop(self, event_filter, poll_interval):
        while True:
            for event in event_filter.get_new_entries():
                self.handle_event(event)
                time.sleep(poll_interval)

    def create_agreement(self, addresses, signatures, timestamp, id):
        unicorn_txn = self.contract.functions.createAgreement(
        id,
        addresses,
        signatures,
        timestamp).buildTransaction({
        'gas': 300000,
        'gasPrice': self.web3.toWei('1', 'gwei'),
        "from": Web3.toChecksumAddress('F4B5dbF1BC65cA8897a4e375ee42046765551D9F'),
        'nonce': self.web3.eth.getTransactionCount(Web3.toChecksumAddress('F4B5dbF1BC65cA8897a4e375ee42046765551D9F'))
        })
        signed_txn = self.web3.eth.account.defaultAccount.signTransaction(unicorn_txn)
        self.web3.eth.sendRawTransaction(signed_txn.rawTransaction)

    def get_all_agreements(self, addresses, id):
        unicorn_txn = self.contract.functions.getAgreementResult(
        id,
        addresses).buildTransaction({
        'gas': 3000000,
        'gasPrice': self.web3.toWei('1', 'gwei'),
        "from": Web3.toChecksumAddress('F4B5dbF1BC65cA8897a4e375ee42046765551D9F'),
        'nonce': self.web3.eth.getTransactionCount(Web3.toChecksumAddress('F4B5dbF1BC65cA8897a4e375ee42046765551D9F'))
        })
        signed_txn = self.web3.eth.account.defaultAccount.signTransaction(unicorn_txn)
        res = self.web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        time.sleep(10)
        not_found = True
        while (not_found):
            try:
                time.sleep(10)
                receipt = self.web3.eth.getTransactionReceipt(res)
                event_filter = self.contract.events.AgreementsReturn().processReceipt(receipt)
                print(event_filter)
                not_found = False
            except:
                pass

    def get_special_agreements(self, addresses, timestamp, id):
        unicorn_txn = self.contract.functions.getSpecialAgreementResult(
        id,
        addresses,
        timestamp).buildTransaction({
        'gas': 3000000,
        'gasPrice': self.web3.toWei('1', 'gwei'),
        "from": Web3.toChecksumAddress('F4B5dbF1BC65cA8897a4e375ee42046765551D9F'),
        'nonce': self.web3.eth.getTransactionCount(Web3.toChecksumAddress('F4B5dbF1BC65cA8897a4e375ee42046765551D9F'))
        })
        signed_txn = self.web3.eth.account.defaultAccount.signTransaction(unicorn_txn)
        res = self.web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        not_found = True
        while (not_found):
            try:
                time.sleep(10)
                receipt = self.web3.eth.getTransactionReceipt(res)
                event_filter = self.contract.events.SpecialAgreementReturn().processReceipt(receipt)
                print(event_filter)
                not_found = False
            except:
                pass

if __name__ == '__main__':
    pass
    contract = ContractHandler("b665c565737aa50cbcb0807a4e51f12f88d56902")
    #contract.create_agreement([Web3.toChecksumAddress("14723a09acff6d2a60dcdf7aa4aff308fddc160c"),Web3.toChecksumAddress("583031d1113ad414f02576bd6afabfb302140225")],[423432,43242], 1355563265, 11)
    contract.get_all_agreements([Web3.toChecksumAddress("14723a09acff6d2a60dcdf7aa4aff308fddc160c"),Web3.toChecksumAddress("583031d1113ad414f02576bd6afabfb302140225")], 11)
    #contract.get_special_agreements([Web3.toChecksumAddress("14723a09acff6d2a60dcdf7aa4aff308fddc160c"),Web3.toChecksumAddress("583031d1113ad414f02576bd6afabfb302140225")], 1355563265, 11)

# dir_path = path.dirname(path.realpath(__file__))
# web3 = Web3(HTTPProvider("https://ropsten.infura.io/v3/52a597c1982940f0b7367628415eeb8d"))
# with open(str(path.join(dir_path, 'contract_abi.json')), 'r') as abi_definition:
    # abi = json.load(abi_definition)
# contract = web3.eth.contract(abi, contract_address)
