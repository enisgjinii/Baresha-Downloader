@echo off
echo Baresha Downloader - Installer
echo ==============================

REM Create installation directory
set INSTALL_DIR=%PROGRAMFILES%\Baresha-Downloader
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

REM Copy executable
copy "dist\Baresha-Downloader.exe" "%INSTALL_DIR%\"

REM Create desktop shortcut
set DESKTOP=%USERPROFILE%\Desktop
echo @echo off > "%DESKTOP%\Baresha-Downloader.bat"
echo start "" "%INSTALL_DIR%\Baresha-Downloader.exe" >> "%DESKTOP%\Baresha-Downloader.bat"

REM Create start menu shortcut
set START_MENU=%APPDATA%\Microsoft\Windows\Start Menu\Programs
if not exist "%START_MENU%\Baresha-Downloader" mkdir "%START_MENU%\Baresha-Downloader"
echo @echo off > "%START_MENU%\Baresha-Downloader\Baresha-Downloader.bat"
echo start "" "%INSTALL_DIR%\Baresha-Downloader.exe" >> "%START_MENU%\Baresha-Downloader\Baresha-Downloader.bat"

echo Installation completed!
echo The application has been installed to: %INSTALL_DIR%
echo Desktop shortcut created.
echo Start menu shortcut created.
pause
