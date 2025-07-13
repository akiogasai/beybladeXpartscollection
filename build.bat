@echo off
echo Building Beyblade X Manager...
pyinstaller --onefile --windowed --name "BeybladeX_Manager" --distpath "./release" --workpath "./build_temp" --specpath "./build_temp" main.py
echo Build complete! Check the 'release' folder for your executable.
pause
