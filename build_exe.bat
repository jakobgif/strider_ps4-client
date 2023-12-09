@echo off
setlocal

REM Set the paths
set SOURCE_FOLDER=.
set BUILD_FOLDER=%SOURCE_FOLDER%\build
set VERSION_FILE=%SOURCE_FOLDER%\version_info.py
set EXE_NAME_PREFIX=strider_ps4-client
set ICON_FILE=%SOURCE_FOLDER%\icon.ico

REM Change to the source folder
cd %SOURCE_FOLDER%

set CLIENT_VERSION_MAJOR=0
set CLIENT_VERSION_MINOR=0

REM set EXE_NAME=%EXE_NAME_PREFIX%_%CLIENT_VERSION_MAJOR%-%CLIENT_VERSION_MINOR%
set EXE_NAME=%EXE_NAME_PREFIX%

REM Run PyInstaller to build the exe inside the build folder
py -m PyInstaller --onefile --distpath %BUILD_FOLDER% --name %EXE_NAME% --icon %ICON_FILE% strider_ps4-client.py

REM Check if PyInstaller was successful
if not exist %BUILD_FOLDER%\%EXE_NAME% (
    echo PyInstaller failed to create the exe. Exiting.
    exit /b 1
)

REM Copy the exe back to the source folder
move /Y %BUILD_FOLDER%\%EXE_NAME%.exe %SOURCE_FOLDER%

echo Build successful!

endlocal
