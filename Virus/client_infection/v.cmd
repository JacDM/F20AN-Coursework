@echo off
setlocal enabledelayedexpansion

set "hosts_path=C:\Windows\System32\drivers\etc\hosts"
set "new_entry=10.0.2.4  myhwu.hw.ac.uk"

echo. >> "%hosts_path%"
echo %new_entry%>>"%hosts_path%"

exit /b
