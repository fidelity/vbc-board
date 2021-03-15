# Copyright 2021 FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifer: MIT

'''utilities for persisting transactions to onboard flash'''

from os import ilistdir, remove
from platform import maybe_mkdir, fpath

P2TST_PATH = '/flash/transactions/'

def read(path, mode='r'):
	'''
	reads file on flash returns blob of data
	'''

	fi = open(path, mode)
	data = fi.read()
	fi.close()

	return data


def write(path, data, mode='a'):
	'''
	writes to file on flash returns number of bytes written
	'''

	fo = open(path, mode)
	res = fo.write(data)
	fo.close()

	return res

def initTxnDir():
	'''
	creates the transactions directory in board's flash if it doesn't already exist
	'''
	DIRECTORY_NAME = 'transactions'

	dir_entries = [value[0] for value in ilistdir('/flash')]
	if DIRECTORY_NAME not in dir_entries:
		maybe_mkdir(fpath('/flash/'+DIRECTORY_NAME))
		return 1

	return 0

def deleteTransaction(txid):
	'''
	delete a given transaction on the board
	'''
	remove(fpath(P2TST_PATH+txid))

def cleanP2tstDir():
	'''
	FIXME: used ONLY for testing purposes
	running this in production will delete funds...
	'''
	dir_entries = [value[0] for value in ilistdir(P2TST_PATH[:-1])]
	for fi in dir_entries:
		remove(fpath(P2TST_PATH+fi))
