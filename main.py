# Copyright 2021 FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifer: MIT

'''board initialization and event loop for'''

import uasyncio
from guiHandler import *
from fileHandler import initTxnDir, cleanP2tstDir

TESTING = True

async def loop():
    while True:
        if isUSBReadyToRead():
            result = read_data()

            if result == 0:
                pyb.LED(3).toggle()
                print('error handling. something wrong with reading')

        await uasyncio.sleep_ms(100)

def main():
    #init ializing transactions dir if it does not already exist
    initTxnDir()

    if TESTING:
        #if testing, clean the dev board at each restart of board
        cleanP2tstDir()

    #initializes gui object and the 'main menu'
    gui = GUI()
    gui.screenMainMenu()
    uasyncio.run(loop())

if __name__ == '__main__':
    main()
