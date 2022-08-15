#!/usr/bin/env python

"""BasketballSerialParserCOM.py: Collects data from a Daktronics All Sport 5000 connected via port J2 to a 
Daktronics All Sport CG connected to a computer on COM port (defined on line 32), then parses data to 
a .csv readable by broadcasting programs. This file has only been tested using game code 2101 on a 
Daktronics All Sport 5000 (Volleyball - Match/Game).
"""

__author__ = "Collin Moore"
__copyright__ = "Copyright 2021, Bristol Tennessee City Schools"
__credits__ = "Collin Moore"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Collin Moore"
__email__ = "moorec@btcs.org"
__status__ = "Release"


#Set your COM Port name here:
COMPort = 'COM9'


#Import PySerial
import serial
#Open defined COM port and reset input buffer
ser = serial.Serial(COMPort, 9600)
ser.reset_input_buffer()

while True:
	#read 45 bits from serial input
	res = ser.read(39)

	#encode characters to unicode for variables without functions
	homeScore = chr(res[9]) + chr(res[10])
	guestScore = chr(res[11]) + chr(res[12])
	homeSets = chr(res[17])
	guestSets = chr(res[18])
	setNumber = chr(res[19])
	homeSetScore1 = chr(res[20]) + chr(res[21])
	homeSetScore2 = chr(res[22]) + chr(res[23])
	homeSetScore3 = chr(res[24]) + chr(res[25])
	homeSetScore4 = chr(res[26]) + chr(res[27])
	guestSetScore1 = chr(res[28]) + chr(res[29])
	guestSetScore2 = chr(res[30]) + chr(res[31])
	guestSetScore3 = chr(res[32]) + chr(res[33])
	guestSetScore4 = chr(res[34]) + chr(res[35])


	#Saves formatted data to variable in CSV format.
	#"EOF" exists to mark end of file - potential empty columns at end were causing readability issues in vMix
	scoreboardData = (homeScore + "," + guestScore + "," + homeSets + "," + guestSets + "," + "SET " + setNumber + "," + 
					  homeSetScore1 + "," + homeSetScore2 + "," + homeSetScore3 + "," + homeSetScore4 + "," + 
					  guestSetScore1 + "," + guestSetScore2 + "," + guestSetScore3 + "," + guestSetScore4 + "," + "EOF")
	#Open/Create CSV data file for writing
	scoreboardDataFile = open("VolleyballDataFile.csv", "w")
	#saves and closes CSV file
	scoreboardDataFile.write(scoreboardData)
	scoreboardDataFile.close()


	#Prints data sets for debugging. Can comment out when running script.
	print(res)
	print(scoreboardData)
    