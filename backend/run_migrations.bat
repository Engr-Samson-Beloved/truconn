@echo off
echo ========================================
echo Running Compliance Migrations
echo ========================================
echo.

REM Check if venv exists and activate it
if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
) else if exist "backend\venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call backend\venv\Scripts\activate.bat
) else (
    echo WARNING: Virtual environment not found!
    echo Please activate it manually first.
    echo.
)

echo.
echo Running migrations for compliance app...
python manage.py migrate compliance

echo.
echo Running all migrations to ensure everything is up to date...
python manage.py migrate

echo.
echo ========================================
echo Migration Complete!
echo ========================================
pause

