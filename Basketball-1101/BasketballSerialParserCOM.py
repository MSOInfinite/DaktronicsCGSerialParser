#!/usr/bin/env python

"""BasketballSerialParserCOM.py: Collects data from a Daktronics All Sport 5000 connected via one of the J ports to a 
Daktronics All Sport CG connected to a computer COM port, then parses data to a .csv readable by broadcasting programs.
This file has only been tested using game code 1101 on a Daktronics All Sport 5000 (Basketball - Player-Foul).
"""

__author__ = "Collin Moore"
__copyright__ = "Copyright 2020, Bristol Tennessee City Schools"
__credits__ = "Collin Moore"
__license__ = "MIT"
__version__ = "1.5"
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

def foulBonuser(foulsTens, foulsOnes):
	"""Returns string with 'B' if fouls is 7 or greater"""
	foulsStr = chr(foulsTens) + chr(foulsOnes)
	foulsInt = int(foulsStr)
	bonus = ""

	if foulsInt >= 7:
		bonus = "B"

	return(bonus)


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

	#encode characters to unicode for variables without functions
	timeText = chr(res[1]) + chr(res[2]) + chr(res[3]) + chr(res[4]) + chr(res[5]) + chr(res[6]) + chr(res[7])
	homeScore = chr(res[14]) + chr(res[15])
	guestScore = chr(res[17]) + chr(res[18])
	timeoutTime = chr(res[30]) + chr(res[31]) + chr(res[32]) + chr(res[33]) + chr(res[34])

	#Call functions and assign values
	quarterText = intSuffixer(res[29])
	homeBonus = foulBonuser(res[21], res[22])
	awayBonus = foulBonuser(res[19], res[20])


	#Saves formatted data to variable in CSV format.
	#"EOF" exists to mark end of file - potential empty columns at end were causing readability issues in vMix
	scoreboardData = (timeText + "," + homeScore + "," + guestScore + "," + homeBonus + "," + awayBonus + "," + quarterText + "," + timeoutTime + "," + "EOF")
	#Open/Create CSV data file for writing
	scoreboardDataFile = open("BasketballDataFile.csv", "w")
	#saves and closes CSV file
	scoreboardDataFile.write(scoreboardData)
	scoreboardDataFile.close()


	#Prints data sets for debugging. Can comment out when running script.
	print(res)
	print(scoreboardData)
    