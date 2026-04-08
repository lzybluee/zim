@echo off
setlocal enabledelayedexpansion

set zim_list=

for %%f in ("%~dp0\*.zim") do (
	set zim_list=!zim_list! "%%f"
)

"%~dp0\kiwix-tools\kiwix-serve.exe" -v -p 8080 !zim_list!

endlocal