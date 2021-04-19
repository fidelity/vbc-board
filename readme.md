# DISCLAIMER

This code is not production ready. DO NOT USE WITH MAINNET. DO NOT USE REAL FUNDS.

# vbc-board

vbc-board is the code for the development board that is used in conjunction with [vbc-desktop](https://github.com/fidelity/vbc-desktop)

# Tools and Preparation

You will need the [STM32F469NI MCU](https://www.st.com/en/evaluation-tools/32f469idiscovery.html) and will also need to grasp a basic understanding of [micropython](https://micropython.org/).

<img width="322" alt="Screen Shot 2021-04-19 at 1 11 38 PM" src="https://user-images.githubusercontent.com/64624962/115276443-04160500-a111-11eb-8bdd-f2e69bd478b9.png">

It is advised to watch the first three videos of this video series provided by cryptoadvance to learn how to use micropython with this board, as well how to boot firmware on this device.

0. <https://www.youtube.com/watch?v=Rr4iZ5WOFYo>
1. <https://www.youtube.com/watch?v=AgOqTGeDrac>
2. <https://www.youtube.com/watch?v=zoYpcuibRh4>

# Board setup

The board should be connected via both the STLink and MicroUSB plugs. The [MicroPython bundle](https://github.com/diybitcoinhardware/f469-disco/releases/tag/v1.1.2) should be loaded by copying it the drive DIS_F469NI, as shown in the diyhardware video #2. The drive PYBQSPI may appear automatically. If not, unmount and remount the board.

# Run the code

Once you've done the preparation, simply clone this repository and drag all the files into the PYBQSPI volume that appears on your machine.
You will see two volumes, DIS_F469NI and PYBQSPI, the volume that handles the files from this repository is PYBQSPI.

# Run with vbc-desktop

Now that your development board is prepared, go to vbc-desktop to learn how to run the vbc program!
