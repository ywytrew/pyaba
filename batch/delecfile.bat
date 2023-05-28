echo Starting WinSCP
"C:\Program Files (x86)\WinSCP\Winscp.com" /script="D:\gitproject\pyaba\batch\delectfile.txt" /log=winscp.log /ini=nul 
echo WinSCP finished

if %ERRORLEVEL% neq 0 goto error
 
echo File %REMOTE_PATH% exists
rem Do something
exit /b 0
 
:error
echo Error or file %REMOTE_PATH% not exists
exit /b 1