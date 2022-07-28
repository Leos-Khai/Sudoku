@echo off
if exist main.build\ (
    rmdir /s /q main.build
)
if exist main.dist\ (
    rmdir /s /q main.dist\
)
echo Generating excecutable
python -m nuitka --quiet --standalone --python-flag=no_site --windows-disable-console src\main.py
echo Moving lib and data files
xcopy /E /I /Q libs main.dist
xcopy /E /I /Q src\data main.dist\data
xcopy /E /I /Q src\sounds main.dist\sounds
::rename main.dist\main.exe Sudoku.exe
echo Done
