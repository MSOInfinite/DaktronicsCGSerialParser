# Baseball | Game code 5501
.csv columns are as follows: Home Score , Away Score , Inning , Home Hits , Away Hits , Home Errors , Away Errors , 
Home Score 1st Inning , Away Score 1st Inning , Home Score 2nd Inning , Away Score 2nd Inning , Home Score 3rd Inning , Away Score 3rd Inning , 
Home Score 4th Inning , Away Score 4th Inning , Home Score 5th Inning , Away Score 5th Inning , Home Score 6th Inning , Away Score 6th Inning , 
Home Score 7th Inning , Away Score 7th Inning , Home Score 8th Inning , Away Score 8th Inning , Home Score 9th Inning , Away Score 9th Inning , 
Home Score 10th Inning , Away Score 10th Inning , Ball-Strike , Out# Out , EOF

Inning is in column 3 and is formatted as TopBot Inning#  EX: "Bot 1st"  This uses logic based on when "out == 3" top flip Top and Bot, so your 
scoreboard operator needs to avoid errantly setting outs to 3 or this will cause issues with the inning display.

Balls and Strikes are in column 28, and is formatted Ball-Strike  EX: "3-2"

Outs are in column 29 and is formatted Out# Out  EX: "3 Out"
