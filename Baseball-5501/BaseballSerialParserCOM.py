#!/usr/bin/env python

"""SoccerSerialParserCOM.py: Collects data from a Daktronics All Sport 5000 connected via port J2 to a 
Daktronics All Sport CG connected to a computer on COM port (defined on line 56), then parses data to 
a .csv readable by broadcasting programs. This file has only been tested using game code 5501 on a 
Daktronics All Sport 5000 (Baseball - Standard).
"""

__author__ = "Collin Moore"
__copyright__ = "Copyright 2021, Bristol Tennessee City Schools"
__credits__ = "Collin Moore"
__license__ = "MIT"
__version__ = "1.1.2"
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
def intSuffixer(passedTens, passedOnes):
	"""Returns string with passed int value and corresponding suffix. Anything outside characters 1-4 returns the int value."""
	intSuffix = chr(passedTens) + chr(passedOnes)
	if passedOnes == 49:
		intSuffix += "st"
	elif passedOnes == 50:
		intSuffix += "nd"
	elif passedOnes == 51:
		intSuffix += "rd"
	elif passedOnes >= 52:
		intSuffix += "th"

	return(intSuffix)

def topBotFlipper(topBot):
    """When called, flips topBot from 'Top' to 'Bot' or vice-versa. This is a pretty rough method at the time. If your scoreboard
    operator errantly sets outs to 3, this will flip and cause your innings to be off."""
    if topBot == "Top":
        topBot = "Bot"
    elif topBot == "Bot":
        topBot = "Top"
    
    return(topBot)

#Set your COM Port name here:
COMPort = 'COM4'


#Import PySerial
import serial
#Open defined COM port and reset input buffer
ser = serial.Serial(COMPort, 9600)
ser.reset_input_buffer()
#Set topBot to Top by default from program start, and logic to know if flipping process has completed
topBot = "Top"
inningFlipped = False

while True:
	#read 50 bits from serial input
	res = ser.read(169)


	#encode characters to unicode for variables without functions
	homeScore = chr(res[3]) + chr(res[4])
	guestScore = chr(res[7]) + chr(res[8])
	homeHits = chr(res[29]) + chr(res[30])
	guestHits = chr(res[35]) + chr(res[36])
	homeErrors = chr(res[32])
	guestErrors = chr(res[38])
	homeFirst = chr(res[85])
	guestFirst = chr(res[109])
	homeSecond = chr(res[87])
	guestSecond = chr(res[111])
	homeThird = chr(res[89])
	guestThird = chr(res[113])
	homeFourth = chr(res[91])
	guestFourth = chr(res[115])
	homeFifth = chr(res[93])
	guestFifth = chr(res[117])
	homeSixth = chr(res[95])
	guestSixth = chr(res[119])
	homeSeventh = chr(res[97])
	guestSeventh = chr(res[121])
	homeEighth = chr(res[99])
	guestEighth = chr(res[123])
	homeNinth = chr(res[101])
	guestNinth = chr(res[125])
	homeTenth = chr(res[103])
	guestTenth = chr(res[127])
	ball = chr(res[48])
	strike = chr(res[49])
	out = chr(res[50])
    

	#Check if Outs have progressed to 3, and call topBotFlipper to swap inning segment
	if out == "3" and inningFlipped == False:
			topBot = topBotFlipper(topBot)
			inningFlipped = True

    
	#Reset inningFlipped once "out" is reset to "0"
	if out == "0" and inningFlipped:
		inningFlipped = False
	
	#Call functions and assign values
	quarterText = topBot + intSuffixer(res[14], res[15])

	#Saves formatted data to variable in CSV format.
	#"EOF" exists to mark end of file - potential empty columns at end were causing readability issues in vMix
	scoreboardData = (homeScore + "," + guestScore + "," + quarterText + "," + homeHits + "," + guestHits + ","
		+ homeErrors + "," + guestErrors + "," + guestFirst + "," + homeFirst + "," + guestSecond + "," 
		+ homeSecond + "," + guestThird + ","  + homeThird + "," + guestFourth + "," + homeFourth + "," 
		+ guestFifth + "," + homeFifth + "," + guestSixth + "," + homeSixth + "," + guestSeventh + "," 
		+ homeSeventh + "," + guestEighth + "," + homeEighth + "," + guestNinth + "," + homeNinth + "," 
		+ guestTenth + "," + homeTenth + "," + ball + "-"  + strike + "," + out + " Out," + "EOF")
	#create/overwrite CSV data file
	scoreboardDataFile = open("BaseballDataFile.csv", "w")
	#saves and closes CSV file
	scoreboardDataFile.write(scoreboardData)
	scoreboardDataFile.close()


	#Prints data sets for debugging. Comment out to run the script silently.
	print(res)
	print(scoreboardData)
    