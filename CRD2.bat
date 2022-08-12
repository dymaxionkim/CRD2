REM Anaconda3 Environment
REM set root=%USERPROFILE%\anaconda3
set root=%ProgramData%\anaconda3
call %root%\Scripts\activate.bat %root%
REM call conda env list
call conda activate base

REM Start App
call cd /d D:\git\CRD2\
call python CRD2.py

REM pause
exit