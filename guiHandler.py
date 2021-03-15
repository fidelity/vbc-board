# Copyright 2021 FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifer: MIT

import lvgl as lv
import pyb
import display
from fileHandler import *
from deletedKey import *
from transactionHandler import *
from messageHandler import *

class GUI:
	'''
	this class will be responsible for dealing with the gui/screen when buttons are pressed
	'''

	def __init__(self):
		self.display 	= display.init()
		self.scr 		= lv.scr_act()

	def clear(self):
		'''
		will reset the screen to blank it out 
		will be used inbetween switching gui screens
		'''
		self.scr.clean()


	'''
	GUI Functions
	'''
	def screenMainMenu(self):
		'''
		function to show the 'main menu' : screen shown on board booting up 
		'''
		self.clear()
		
		#welcome text at top of screen
		welcome_label = lv.label(self.scr)
		welcome_label.set_text("Welcome to Encumbered Cold Storage")
		welcome_label.align(None, lv.ALIGN.IN_TOP_MID, 0, 30)

	#FIXME: figure out some more GUI/UI elements for the board