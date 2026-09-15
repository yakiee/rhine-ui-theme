@echo off
setlocal
set "ANDROID_HOME=%~dp0sdk"
set "ANDROID_SDK_ROOT=%~dp0sdk"
set "ANDROID_AVD_HOME=%~dp0avd"
start "Rhine Android Preview" "%~dp0sdk\emulator\emulator.exe" -avd RhinePreview -port 5580 -no-boot-anim -no-metrics -gpu software -feature GLESDynamicVersion
endlocal
