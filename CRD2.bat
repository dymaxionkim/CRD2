REM Miniconda3 Environment in scoop
REM set root=%USERPROFILE%\anaconda3
set root=%userprofile%\scoop\apps\miniconda3\current
call %root%\Scripts\activate.bat
REM call conda env list
REM call conda activate base

REM Start App
call cd /d D:\github\CRD2\
call python CRD2.py

REM pause
exit