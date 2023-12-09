@echo off
setlocal

REM Set the paths
set SOURCE_FOLDER=.
set BUILD_FOLDER=%SOURCE_FOLDER%\build
set EXE_NAME=strider_ps4-client.exe

REM Change to the source folder
cd %SOURCE_FOLDER%

REM Run PyInstaller to build the exe inside the build folder
py -m PyInstaller --onefile --distpath %BUILD_FOLDER% strider_ps4-client.py --icon icon.ico

REM Check if PyInstaller was successful
if not exist %BUILD_FOLDER%\%EXE_NAME% (
    echo PyInstaller failed to create the exe. Exiting.
    exit /b 1
)

REM Copy the exe back to the source folder
move /Y %BUILD_FOLDER%\%EXE_NAME% %SOURCE_FOLDER%

echo Build successful!

endlocal
