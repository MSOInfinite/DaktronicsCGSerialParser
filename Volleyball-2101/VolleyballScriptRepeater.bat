@ECHO off
REM Python Script Repeater
ECHO This script will not end on it's own. Ctrl + C to force-quit
:runScript
python VolleyballSerialParserCOM.py
ECHO Script crashed... Restarting...
GOTO runScript
