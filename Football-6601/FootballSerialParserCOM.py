#!/usr/bin/env python

"""FootballSerialParserCOM5.py: Collects data from a Daktronics All Sport 5000 connected via port J2 to a 
Daktronics All Sport CG connected to a computer COM port, then parses data to a .csv readable by broadcasting programs.
This file has only been tested using game code 6601 on a Daktronics All Sport 5000 (Football - Standard).
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

def ballOnTexter(ballOnTens, ballOnOnes):
	"""Sets ballOnText to blank if no value, or adds "Ball On " if value exists."""
	ballOn = chr(ballOnTens) + chr(ballOnOnes)
	if ballOnOnes == 32:
		ballOnText = ""
	else:
		ballOnText = "Ball On " + ballOn

	return(ballOnText)

def toGoTexter(downInt, toGoTens, toGoOnes):
	"""If Down is blank, skips logic and blanks toGo. Otherwise, will add ' Down' if no data for ballOn, 
	or will add ampersand and parse spacing based on if data exists in 10s place. These steps are for text
	formatting assuming display is formatted to display '1st & 10' normally, with logic to display something 
	like '2nd Down' if data is missing for where the ball is placed."""
	toGo = chr(toGoTens) + chr(toGoOnes)
	if downInt != 32:
		if toGoOnes == 32:
			toGo = " Down"
		elif toGoTens == 32:
			toGo = " &" + toGo
		else:
			toGo = " & " + toGo
	else:
		toGo = ""

	return(toGo)


def timeSecondsChecker(timePunct, time):
	"""Adds leading colon to time if <1 minute."""
	if timePunct == 46:
		timeText = ":" + time
	else:
		timeText = time

	return(timeText)

def POS(POSInt):
	"""Returns 'F' if position indicator is present. The AllSportCG sends a * in a specific position to indicate which
	team has posession, and this changes that character to an 'F'. Using font Mattbats, F is a football."""
	POSText = ""

	if POSInt == 42:
		POSText = "F"

	return(POSText)



#Set your COM Port name here:
COMPort = 'COM7'



#Import PySerial
import serial
#Open defined COM port and reset input buffer
ser = serial.Serial(COMPort, 9600)
ser.reset_input_buffer()

while True:
	#read 45 bits from serial input
	res = ser.read(45)

	#encode characters to unicode for variables without functions (also 'time' because it's so long)
	time = chr(res[1]) + chr(res[2]) + chr(res[3]) + chr(res[4]) + chr(res[5])
	homeScore = chr(res[26]) + chr(res[27])
	guestScore = chr(res[28]) + chr(res[29])

	#Call functions and assign values
	quarterText = intSuffixer(res[30])
	downText = intSuffixer(res[33])
	ballOnText = ballOnTexter(res[31], res[32])
	toGoText = toGoTexter(res[33], res[34], res[35])
	timeText = timeSecondsChecker(res[3], time)
	homePOS = POS(res[36])
	awayPOS = POS(res[37])

	#Saves formatted data to variable in CSV format.
	#"EOF" exists to mark end of file - potential empty columns at end were causing readability issues in vMix
	scoreboardData = (timeText + "," + homeScore + "," + guestScore + "," + quarterText + "," + ballOnText + "," + downText + toGoText + "," + homePOS + "," + awayPOS + "," + "EOF")
	#create/overwrite CSV data file
	scoreboardDataFile = open("FootballDataFile.csv", "w")
	#saves and closes CSV file
	scoreboardDataFile.write(scoreboardData)
	scoreboardDataFile.close()


	#Prints data sets for debugging. Comment out when running script.
	print(res)
	print(scoreboardData)
