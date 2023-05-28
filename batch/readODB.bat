@echo off
REM Change the following path to the location of your ABAQUS
set PATH=C:\SIMULIA\Commands; %PATH%

REM change to the directiory the python script 
D:
cd D:\CAE\pythonProject

REM Run the Abaqus python script
abaqus cae noGUI="ODB_DispStress.py"

pause