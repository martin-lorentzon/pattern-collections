@echo off
setlocal

set "CURR_DIR=%CD%"

:: Extract the directory name from the full path
for %%a in ("%CURR_DIR%") do (
  set "DIR_NAME=%%~na"
)

set "ZIP_NAME=%DIR_NAME%.zip"  REM Use the directory name for the zip file
set "SEVENZIP_PATH=C:\Program Files\7-Zip\7z.exe" REM Replace with your 7-Zip path

:: Create the zip archive with folder structure
"%SEVENZIP_PATH%" a -tzip "%CURR_DIR%\%ZIP_NAME%" "%CURR_DIR%\*" -x!*.bat -x!*.zip -x!*.git*

echo Zip file created: %ZIP_NAME%
pause

endlocal