@echo off
setlocal

REM check admin rights
net session >nul 2>&1
if not %errorLevel% == 0 (
    echo Unable to install: you must run this script as Administrator
    goto end
)

REM Check if Platform Flash Tool is installed (mandatory in order to use ACS)
cflasher --version
if not %errorLevel% == 0 (
    echo "Platform Flash Tool not found !"
    echo "You must install Platform Flash Tool before installing ACS."
    echo "For more details visit Phone flash tool wiki (https://wiki.ith.intel.com/display/DRD/Platform+Flash+Tool)"
    goto end
)

REM get windows version (7 or 8)
for /f "tokens=4-5 delims=. " %%i in ('ver') do set VERSION=%%i.%%j
if "%VERSION%" LEQ "6.1" (
    set DL_COMMAND="(New-Object Net.WebClient).DownloadFile('${url}', '${dest}')"
    set VERSION_NAME=Windows 7
)
if "%VERSION%" GEQ "6.2" (
    set DL_COMMAND="Invoke-WebRequest ${url} -OutFile ${dest}"
    set VERSION_NAME=Windows 8
)

REM detect if python is already installed
set PYTHON_EXEC=""
for /f %%i in ('where python.exe') do set PYTHON_EXEC=%%i
REM check result of 'where python' to see if it contains python.exe
REM eg. replace python.exe by empty string in %PYTHON_EXEC% variable, and check if %PYTHON_EXEC% changed after this
if not %PYTHON_EXEC:python.exe=%==%PYTHON_EXEC% (
    echo Python is already installed in %PYTHON_EXEC%
    goto install_acs
)

REM python is not installed:  download it and install it
set PYTHON_INSTALLER_DEST=%TEMP%\python.msi
set URL="https://mcg-depot.intel.com/artifactory/acs/dependencies/third_parties/tools/Python/python-2.7.8.win32.msi"

echo Running on %VERSION_NAME%
echo downloading %URL%
echo to %PYTHON_INSTALLER_DEST%

REM download python installer through powershell
call set PY_DL_CMD=%%DL_COMMAND:${url}=%URL%%%
call set PY_DL_CMD=%%PY_DL_CMD:${dest}=%PYTHON_INSTALLER_DEST%%%
powershell -Command "%PY_DL_CMD%"

REM install python silently
echo installing python ...
msiexec /i %PYTHON_INSTALLER_DEST% /qn

REM add python to path
set TMP_PYTHON_PATH=C:\Python27\
setx PYTHON_PATH %TMP_PYTHON_PATH%
setx PATH "%%PYTHON_PATH%%;%PATH%"

REM install ACS silently
:install_acs
echo installing ACS ...
%TMP_PYTHON_PATH%python setups/setup_mgr.py install acs_third_parties
if not %errorLevel% == 0 (
    echo Error during install
    goto end
)
%TMP_PYTHON_PATH%python setups/backup_mgr.py backup
if not %errorLevel% == 0 (
    echo Error during install
    goto end
)
%TMP_PYTHON_PATH%python setups/setup_mgr.py uninstall acs_sources
if not %errorLevel% == 0 (
    echo Error during install
    goto end
)
%TMP_PYTHON_PATH%python setups/setup_mgr.py install acs_sources
if not %errorLevel% == 0 (
    echo Error during install
    goto end
)
%TMP_PYTHON_PATH%python setups/backup_mgr.py restore
if not %errorLevel% == 0 (
    echo Error during install
    goto end
)

echo checking ACS installation ...
%TMP_PYTHON_PATH%python check_installation/check_installation.py
if not %errorLevel% == 0 (
    echo Error during install
    goto end
)

:end
endlocal
