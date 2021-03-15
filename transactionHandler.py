# Copyright 2021 FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifer: MIT

'''core logic for TX handling, vaulting and unvaulting'''

from hashlib import sha256
from platform import fpath
from bitcoin import script
from bitcoin import ec
from bitcoin.networks import NETWORKS
from ubinascii import unhexlify, hexlify
from bitcoin.transaction import Transaction, TransactionInput, TransactionOutput
from bitcoin import compact
from deletedKey import *
from fileHandler import *

#key used to sign for authenticated messages
#repeat, not for signing transactions!
device_pk = ec.PrivateKey.from_base58('cUHuRvvWH5PWoWerKWyongmd2a6C5qniVA5PDVYzW9YGkdqwCmV8')

pk = DeletedKey() #the deleted private key used to sign transactions
network = NETWORKS['regtest']

def swapEndian(h):
    '''
    swaps endian of h and hexlifys it
    '''
    data = b''
    for byte in reversed(h):
        data+=bytes([byte])

    return hexlify(data)

def getTxid(tx):
    '''
    bit of a hacky way to generate txid
    micropython does not support [::-1], so we need to call reversed to swap endian
    '''
    return swapEndian(sha256(sha256(tx.serialize()).digest()).digest())

def getAmount(tx):
    amount = 0
    for out in tx.vout:
        amount += out.value

    return amount

def prepareVaultResponse(msg):
    '''
    Prepare Vault response
    will respond with the address of newly generated private key
    alogn with signature of 'signThis'
    '''
    signThis = msg
    pk.generate()
    sig = hexlify(device_pk.sign(signThis).serialize())
    addr = script.p2pkh(pk.get_pubkey()).address(network)

    return [addr, sig]

def finalizeVaultResponse(msg):
    '''
    Finalize Vault response
    reads the unsigned hex of the P2TST, signs and saves it.
    then sends back the txid and value of p2tst to computer

    '''
    unvault_txs = list()
    for tx_hex in msg:
        unvault_tx = Transaction.parse(unhexlify(tx_hex))
        h = unvault_tx.sighash_legacy(0, script.p2pkh(pk.get_pubkey()))
        sig = pk.sign(h)
        unvault_tx.vin[0].script_sig = script.script_sig_p2pkh(sig, pk.get_pubkey())
        unvault_txs.append(unvault_tx)

    # delete the private key, covenant is live!
    pk.delete()
    isDeleted = pk.key is None

    response_list = [isDeleted]
    for unvault_tx in unvault_txs:
        txid = getTxid(unvault_tx).decode('utf8') #changing from bytes to string

        #saving P2TST to storage on board
        PATH = '/flash/transactions/' + str(txid)
        write(fpath(PATH), hexlify(unvault_tx.serialize()))
        response_list.append(txid)
        response_list.append(str(getAmount(unvault_tx)/1e8))

    return response_list

def unvaultResponse(msg):
    '''
    will retrieve the presigned transactions corresponding to list of txids sent by computer
    '''

    res = []
    for txid in msg:
        res.append(read(fpath('/flash/transactions/' + str(txid))))

    return res

def confirmDelete(msg):
    '''
    once the p2tsts are unvaulted, we can delete their hexes from the board
    '''

    for txid in msg:
        deleteTransaction(txid)

    return [True]
