Serial Command Tool

1. Install required package

py -m pip install pyserial

2. Run

py serial_command_tool.py

3. Build EXE

py -m pip install pyinstaller
py -m PyInstaller --onefile --windowed serial_command_tool.py

The exe file will be created in the dist folder.

Usage:
- Select COM port, for example COM9
- Set baudrate, for example 115200
- Enter HEX command, for example FA FF 20 00 00 19
- Press Send Once
