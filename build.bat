@echo off


if exist .\launch.exe (
    del launch.exe
)

pip install pyinstaller

pip install -r requirements.txt

pyinstaller --onefile main.py -n launch -i media/maneki_neko_icon.ico

move .\dist\launch.exe .

rd /s /q .\dist
rd /s /q .\build
del .\launch.spec

if not exist logs (
    mkdir logs
)

if not exist logs\errors.log (
    echo. 2> logs\errors.log
)

if not exist logs\general.log (
    echo. 2> logs\general.log
)

if exist launch.exe (
    echo Build process completed successfully!
) else (
    echo Build process failed!
)

pause