#!/usr/bin/env python

"""BasketballSerialParserCOM.py: Collects data from a Daktronics All Sport 5000 connected via one of the J ports to a 
Daktronics All Sport CG connected to a computer COM port, then parses data to a .csv readable by broadcasting programs.
This file has only been tested using game code 1101 on a Daktronics All Sport 5000 (Basketball - Player-Foul).
"""

__author__ = "Collin Moore"
__copyright__ = "Copyright 2020, Bristol Tennessee City Schools"
__credits__ = "Collin Moore"
__license__ = "MIT"
__version__ = "1.4.1"
__maintainer__ = "Collin Moore"
__email__ = "moorec@btcs.org"
__status__ = "Release"

"""Notes for reading serial bits: pulling individual characters
from 'res' will return integer values assigned to the unicode
character. Characters used for logic checks in this script are:
32 = no data / blank
42 = *
46 = .
49 = 1
50 = 2
51 = 3
52 = 4
"""

#Function definitions
def intSuffixer(passedInt):
	"""Returns string with passed int value and corresponding suffix. Anything outside characters 1-4 returns the int chr."""
	intSuffix = chr(passedInt)
	if passedInt == 49:
		intSuffix += "st"
	elif passedInt == 50:
		intSuffix += "nd"
	elif passedInt == 51:
		intSuffix += "rd"
	elif passedInt == 52:
		intSuffix += "th"

	return(intSuffix)


#Set your COM Port name here:
COMPort = 'COM5'



#Import PySerial
import serial
#Open defined COM port and reset input buffer
ser = serial.Serial(COMPort, 9600)
ser.reset_input_buffer()

while True:
	#read 45 bits from serial input
	res = ser.read(38)

	#encode characters to unicode for variables without functions (also 'time' because it's so long)
	timeText = chr(res[1]) + chr(res[2]) + chr(res[3]) + chr(res[4]) + chr(res[5]) + chr(res[6]) + chr(res[7])
	homeScore = chr(res[14]) + chr(res[15])
	guestScore = chr(res[17]) + chr(res[18])
	homeFouls = chr(res[19]) + chr(res[20])
	awayFouls = chr(res[21]) + chr(res[22])
	timeoutTime = chr(res[30]) + chr(res[31]) + chr(res[32]) + chr(res[33]) + chr(res[34])

	#Call functions and assign values
	quarterText = intSuffixer(res[29])

	#Saves formatted data to variable in CSV format.
	#"EOF" exists to mark end of file - potential empty columns at end were causing readability issues in vMix
	scoreboardData = (timeText + "," + homeScore + "," + guestScore + "," + homeFouls + "," + awayFouls + "," + quarterText + "," + timeoutTime + "," + "EOF")
	#create/overwrite CSV data file
	scoreboardDataFile = open("BasketballDataFile.csv", "w")
	#saves and closes CSV file
	scoreboardDataFile.write(scoreboardData)
	scoreboardDataFile.close()


	#Prints data sets for debugging. Comment out when running script.
	print(res)
	print(scoreboardData)