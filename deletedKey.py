# Copyright 2021 FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifer: MIT

'''implementation of secure key deletion'''

from gc import collect
from hashlib import sha256
from bitcoin import ec
from rng import get_random_bytes

class DeletedKey:
	'''
	an interface to work with a PrivateKey from ec.py to soon be deleted
	'''
	def __init__(self, key=None):
		self.key = key

	def generate(self):
		'''
		generating entropy and initializing private key
		entropy both from RNG chip and analog-to-digital converters on board
		'''

		#creating entropy for private key
		entropy = get_random_bytes(32) + b'lsoeitgmmcnxgwt364495p5,5m5b4g3y344k3jhuri99'
		self.key = ec.PrivateKey.parse(sha256(entropy).digest())

		#garbage collection to ensure the secrets are not in memory
		#FIXME: transition the private key to a bytearray for direct memory access
		del entropy
		collect()

	def delete(self):
		'''
		a prototype of secure key deletion
		'''
		del self.key
		self.key = None
		collect()
		return self.key is None

	def sign(self, msg):
		'''
		sign an arbitrary message with the soon to be deleted private key
		this will be also be used to sign a tx
		return a signature object
		'''
		return self.key.sign(msg)

	def get_pubkey(self):
		'''
		return the public key of the generated key
		'''
		return self.key.get_public_key()

	def isDeleted(self):
		'''
		bool if private key is deleted
		'''
		return self.key is None
