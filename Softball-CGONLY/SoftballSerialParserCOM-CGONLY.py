#!/usr/bin/env python

"""SoftballSerialParserCOM-CGONLY.py: Collects data from a Daktronics All Sport CG connected to a 
computer on COM port (defined on line 47), then parses data to a .csv readable by broadcasting programs. 
This file has only been tested using game mode Baseball on a Daktronics All Sport CG in manual mode.
"""

__author__ = "Collin Moore"
__copyright__ = "Copyright 2021, Bristol Tennessee City Schools"
__credits__ = "Collin Moore"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Collin Moore"
__email__ = "moorec@btcs.org"
__status__ = "Testing"

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
def intSuffixer(passedTens, passedOnes):
	"""Returns string with passed int value and corresponding suffix."""
	intSuffix = chr(passedOnes)
	if passedTens != 32:
		intSuffix = (chr(passedTens) + chr(passedOnes) + "th")
	elif passedOnes == 49:
		intSuffix += "st"
	elif passedOnes == 50:
		intSuffix += "nd"
	elif passedOnes == 51:
		intSuffix += "rd"
	elif passedOnes >= 52:
		intSuffix += "th"

	return(intSuffix)

#Set your COM Port name here:
COMPort = 'COM3'


#Import PySerial
import serial
#Open defined COM port and reset input buffer
ser = serial.Serial(COMPort, 9600)
ser.reset_input_buffer()

while True:
	#read 50 bits from serial input
	res = ser.read(169)


	#encode characters to unicode for variables without functions
	homeScore = chr(res[3]) + chr(res[4])
	guestScore = chr(res[7]) + chr(res[8])
	ball = chr(res[48])
	strike = chr(res[49])
	out = chr(res[50])
	topBot = (chr(res[15]) + chr(res[16]) + chr(res[17]) + " ")
	
	#Call functions and assign values
	quarterText = topBot + intSuffixer(res[9], res[10])

	#Saves formatted data to variable in CSV format.
	#"EOF" exists to mark end of file - potential empty columns at end were causing readability issues in vMix
	scoreboardData = (homeScore + "," + guestScore + "," + quarterText + "," + ball + "-"  + strike + "," + out + " Out," + "EOF")
	#create/overwrite CSV data file
	scoreboardDataFile = open("SoftballDataFile.csv", "w")
	#saves and closes CSV file
	scoreboardDataFile.write(scoreboardData)
	scoreboardDataFile.close()


	#Prints data sets for debugging. Comment out to run the script silently.
	print(res)
	print(scoreboardData)
    