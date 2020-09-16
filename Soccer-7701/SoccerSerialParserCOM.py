#!/usr/bin/env python

"""SoccerSerialParserCOM.py: Collects data from a Daktronics All Sport 5000 connected via port J2 to a 
Daktronics All Sport CG connected to a computer on COM port (defined on line 58), then parses data to 
a .csv readable by broadcasting programs. This file has only been tested using game code 7701 on a 
Daktronics All Sport 5000 (Soccer - Standard).
"""

__author__ = "Collin Moore"
__copyright__ = "Copyright 2020, Bristol Tennessee City Schools"
__credits__ = "Collin Moore"
__license__ = "GPL"
__version__ = "1.2.0"
__maintainer__ = "Collin Moore"
__email__ = "25944818+MSOInfinite@users.noreply.github.com"
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
	"""Returns string with passed int value and corresponding suffix. Anything outside characters 1-4 returns the int value."""
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
COMPort = 'COM7'


#Import PySerial
import serial
#Open defined COM port and reset input buffer
ser = serial.Serial(COMPort, 9600)
ser.reset_input_buffer()

while True:
	#read 50 bits from serial input
	res = ser.read(50)

	#encode characters to unicode for variables without functions (also 'time' because it's so long)
	timeText = chr(res[1]) + chr(res[2]) + chr(res[3]) + chr(res[4]) + chr(res[5])
	homeScore = chr(res[26]) + chr(res[27])
	guestScore = chr(res[28]) + chr(res[29])

	#Call functions and assign values
	quarterText = intSuffixer(res[30])

	#Saves formatted data to variable in CSV format.
	#"EOF" exists to mark end of file - potential empty columns at end were causing readability issues in vMix
	scoreboardData = (timeText + "," + homeScore + "," + guestScore + "," + quarterText + "," + "EOF")
	#create/overwrite CSV data file
	scoreboardDataFile = open("SoccerDataFile.csv", "w")
	#saves and closes CSV file
	scoreboardDataFile.write(scoreboardData)
	scoreboardDataFile.close()


	#Prints data sets for debugging. Comment out to run the script silently.
	print(res)
	print(scoreboardData)