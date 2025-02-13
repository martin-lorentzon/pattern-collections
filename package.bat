@echo off
setlocal

set "CURR_DIR=%CD%"

:: Extract the directory name from the full path
for %%a in ("%CURR_DIR%") do (
  set "DIR_NAME=%%~na"
)

:: Prompt the user for a version number
set /p "VERSION=Enter version number (e.g., 1_0, 2_1, or leave blank): "

:: Add the version suffix to the directory name if provided
if not "%VERSION%"=="" (
  set "DIR_NAME=%DIR_NAME%_%VERSION%"
)

set "ZIP_NAME=%DIR_NAME%.zip"  REM Use the directory name (with version) for the zip file
set "SEVENZIP_PATH=C:\Program Files\7-Zip\7z.exe" REM Replace with your 7-Zip path

:: Create the zip archive with folder structure
"%SEVENZIP_PATH%" a -tzip "%CURR_DIR%\%ZIP_NAME%" "%CURR_DIR%\*" -x!*.bat -x!*.zip -x!*.git*

echo Zip file created: %ZIP_NAME%
pause

endlocal