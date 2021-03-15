# Copyright 2021 FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifer: MIT

'''
Message IDs: Corresponding Messages
0			: PrepareVault(signThis) - computer sends, board receives
1			: PrepareVaultResponse(Address, sig(signThis)) - board sends, computer receives
2			: FinalizeVault(unsigned P2TST)	- computer sends, board receives
3			: FinalizeVaultResponse(txid, isDeleted) - board sends, computer receives
4			: UnvaultRequest([txid_list]) - computer sends, board recieves
5			: UnvaultResponse([[p2tst_list]]) - board sends, computer receives
6			: ConfirmDelete() - computer sends, board recieves
7			: ConfirmDeleteResponse()	- board sends, computer receives
'''
#lightweight implementation of serial communication protocol
import time
from pyb import USB_VCP
from transactionHandler import *


CONSTANT	= '___' #divider between msg id and message
MSG_DIVIDER	= '##?' #divider between parts of the data
BUFFER_LEN	= 1024	#size of board's read buffer

#setting up USB comms
usb = USB_VCP()

def serializeField(data):
	'''
	will serialize a value depending on its data type
	messages need to be serialized before being sent over usb
	'''
	if isinstance(data, bytes):
		return data
	elif isinstance(data, str):
		return bytes(data, 'utf8')
	elif (isinstance(data, int)) or (isinstance(data, bool)):
		return bytes([data])
	else:
		print('unrecgonized data type...')
		return False

def isUSBReadyToRead():
	return usb.any()

def read_data():
	buffer = b''
	buffer += usb.recv(BUFFER_LEN, timeout=1000)
	time.sleep_ms(50)

	#checking if the first character of the message is an integer(message ID) and that the second character is an underscore
	#if not, it is an unrecongzed message and should be ignored
	if (isinstance(buffer[0]) != int) or (buffer[1] != 95):
		return 0

	unpack_data(buffer)

def send_data(buffer):
	usb.send(buffer)

def unpack_data(buffer):

	# print("Received:\t", buffer)

	#unpacking the message header
	decoded_msg = buffer.decode('utf8').split(CONSTANT)
	msgId = int.from_bytes(bytes(decoded_msg[0], 'utf8'), 'big') #decode the msgId

	split_msg = decoded_msg[1].split(MSG_DIVIDER)
	split_msg = split_msg[:-1]

	#depending on what the message id is, we call a different function
	if msgId == 0:
		prepareVault_handler(split_msg)

	elif msgId == 2:
		finalizeVault_handler(split_msg)

	elif msgId == 4:
		unvault_handler(split_msg)

	elif msgId == 6:
		confirmDelete_handler(split_msg)

	else:
		print("unidentified msg id")
		return 1

def pack_data(msg, msgId):

	#preparing the message to be sent back to computer
	buffer = bytes([msgId]) + bytes(CONSTANT, 'utf8')

	#need to split up data to differentiate objects in message
	for field in msg:
		buffer += serializeField(field)
		buffer += bytes(MSG_DIVIDER, 'utf8')

	buffer += bytes('\n', 'utf8')

	# print("Sent:\t", buffer)

	send_data(buffer)

def prepareVault_handler(msg):
	signThis = msg[0]
	res = prepareVaultResponse(signThis)
	pack_data(res, 1)

def finalizeVault_handler(msg):
	res = finalizeVaultResponse(msg)
	pack_data(res, 3)

def unvault_handler(msg):
	res = unvaultResponse(msg)
	pack_data(res, 5)

def confirmDelete_handler(msg):
	res = confirmDelete(msg)
	pack_data(res, 7)
