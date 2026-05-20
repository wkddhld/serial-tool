@echo off
py -m pip install pyserial pyinstaller
py -m PyInstaller --onefile --windowed serial_command_tool.py
pause
