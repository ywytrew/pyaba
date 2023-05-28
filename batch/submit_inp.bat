@echo off
REM Change the following path to the location of your ABAQUS
set PATH=C:\SIMULIA\Commands; %PATH%

REM change to the directiory the python script 
D:
cd D:\CAE\pythonProject

REM sumbit the job to abqus
abaqus job=Job-1 input=Job-1.inp

:wait_for_completion
REM Wait for 10 seconds before checking the job status
timeout /t 10 /nobreak

REM Check if the .sta file exists and contains the "COMPLETED" status
findstr /m /c:"COMPLETED" Job-1.sta >nul 2>&1
if %errorlevel%==0 (
    echo Job completed successfully.
    goto :end
) else (
    echo Waiting for job to complete...
    goto :wait_for_completion
)

:end

pause