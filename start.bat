@echo off
setlocal DisableDelayedExpansion
rem Open the checked-in reader snapshot without rebuilding or installing dependencies.
pushd "%~dp0"
if errorlevel 1 goto path_error
set "PYTHONDONTWRITEBYTECODE=1"

".conda-env\python.exe" -I -B -c "import sys; sys.exit(sys.version_info < (3, 8))" >nul 2>&1
if not errorlevel 1 (
  set "READER_PYTHON=.conda-env\python.exe"
  goto launch
)
".venv\Scripts\python.exe" -I -B -c "import sys; sys.exit(sys.version_info < (3, 8))" >nul 2>&1
if not errorlevel 1 (
  set "READER_PYTHON=.venv\Scripts\python.exe"
  goto launch
)
py -3 -I -B -c "import sys; sys.exit(sys.version_info < (3, 8))" >nul 2>&1
if not errorlevel 1 goto launch_py
python3 -I -B -c "import sys; sys.exit(sys.version_info < (3, 8))" >nul 2>&1
if not errorlevel 1 (
  set "READER_PYTHON=python3"
  goto launch
)
python -I -B -c "import sys; sys.exit(sys.version_info < (3, 8))" >nul 2>&1
if not errorlevel 1 (
  set "READER_PYTHON=python"
  goto launch
)
echo Python 3.8+ was not found. Install Python 3 or provide a project-local Python environment.
set "READER_EXIT=1"
goto finish

:launch
"%READER_PYTHON%" -I -B "scripts\start-reader.py" %*
set "READER_EXIT=%ERRORLEVEL%"
goto finish

:launch_py
py -3 -I -B "scripts\start-reader.py" %*
set "READER_EXIT=%ERRORLEVEL%"
goto finish

:path_error
echo Cannot open the project directory.
pause
exit /b 1

:finish
popd
if not "%READER_EXIT%"=="0" pause
exit /b %READER_EXIT%
