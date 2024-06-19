#copy following files to the dist/adc directory
@echo off
REM Create the dist/adc directory if it doesn't exist
if not exist "dist\adc" mkdir "dist\adc"

REM Copy the files
copy "adeko.ico" "dist\adc"
copy "cr.py" "dist\adc"
copy "db.db" "dist\adc"
copy "dd.py" "dist\adc"
copy "md.ui" "dist\adc"
copy "ed.py" "dist\adc"
copy "ops.py" "dist\adc"
copy "otd.py" "dist\adc"
copy "su.py" "dist\adc"
