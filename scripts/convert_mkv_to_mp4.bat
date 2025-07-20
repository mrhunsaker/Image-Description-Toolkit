@echo off
        setlocal enabledelayedexpansion

REM HandBrake CLI MKV to MP4 Converter
REM This script converts all MKV files in current directory and subdirectories to MP4
REM Preserves all audio, video, and subtitle tracks
REM Output files are named using the parent directory name + sequential number
REM Example: c:\movies\anothera\title4.mkv becomes anothera01.mp4

REM ========================================
REM TEST MODE TOGGLE - Change to enable/disable testing
REM Set to 1 for testing (no actual conversion)
REM Set to 0 for actual conversion
set "TESTMODE=0"
REM ========================================

echo HandBrake MKV to MP4 Converter
if %TESTMODE% equ 1 (
    echo [TESTING MODE ENABLED - No actual conversions will be performed]
)
echo.

REM Check if HandBrakeCLI is available
where HandBrakeCLI >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: HandBrakeCLI not found in PATH
    echo Please install HandBrake and add HandBrakeCLI.exe to your PATH
    pause
    exit /b 1
)

REM Create output directory
if not exist "converted" mkdir "converted"

REM Create log file with timestamp
set "logfile=conversion_log_%date:~-4,4%-%date:~-10,2%-%date:~-7,2%_%time:~0,2%-%time:~3,2%-%time:~6,2%.txt"
set "logfile=%logfile: =0%"
echo HandBrake MKV to MP4 Conversion Log > "%logfile%"
echo Started: %date% %time% >> "%logfile%"
echo. >> "%logfile%"

echo Scanning for MKV files...
echo.

REM First pass: Show all files that will be processed
echo Files to be processed:
echo =====================
echo Files to be processed: >> "%logfile%"
echo ===================== >> "%logfile%"
set "filecount=0"
for /r %%F in (*.mkv) do (
    set /a "filecount+=1"
    echo !filecount!. %%F
    echo !filecount!. %%F >> "%logfile%"
)

if !filecount! equ 0 (
    echo No MKV files found in current directory or subdirectories.
    echo No MKV files found in current directory or subdirectories. >> "%logfile%"
    echo Check log file: %logfile%
    pause
    exit /b 0
)

echo.
echo Total files found: !filecount!
echo Log file: %logfile%
echo.
echo Converting MKV files to MP4...
echo.
echo. >> "%logfile%"
echo Total files found: !filecount! >> "%logfile%"
echo. >> "%logfile%"
echo Converting MKV files to MP4... >> "%logfile%"
echo. >> "%logfile%"

REM Initialize directory counter array
set "dircount="

REM Process all MKV files recursively
for /r %%F in (*.mkv) do (
    echo Processing: %%~nxF
    echo Processing: %%F >> "%logfile%"
    
    REM Get the directory path of the current file
    set "filedir=%%~dpF"
    
    REM Extract the last directory name from the path
    REM Remove trailing backslash and get the last directory name
    set "filedir=!filedir:~0,-1!"
    for %%D in ("!filedir!") do set "dirname=%%~nxD"
    
    REM Remove any spaces and special characters from dirname and convert to lowercase
    set "dirname=!dirname: =!"
    set "dirname=!dirname:-=!"
    set "dirname=!dirname:_=!"
    
    REM Fallback if dirname is empty (file in root directory)
    if "!dirname!"=="" set "dirname=root"
    
    REM Get current counter for this directory
    set "counter=!dircount[!dirname!]!"
    if "!counter!"=="" set "counter=0"
    
    REM Find the next available filename
    :find_next_filename
    set /a "counter+=1"
    
    REM Format counter with leading zero
    if !counter! lss 10 (
        set "counterstr=0!counter!"
    ) else (
        set "counterstr=!counter!"
    )
    
    REM Create output filename using directory name + counter
    set "output=converted\!dirname!!counterstr!.mp4"
    
    REM Check if file already exists, if so increment counter and try again
    if exist "!output!" goto find_next_filename
    
    REM Update the counter for this directory
    set "dircount[!dirname!]=!counter!"
    
    echo Will be saved as: !dirname!!counterstr!.mp4
    echo Will be saved as: !dirname!!counterstr!.mp4 >> "%logfile%"
    
    REM Create output directory if needed
    if not exist "converted" mkdir "converted"
    
    REM Log start time
    echo Start time: %date% %time% >> "%logfile%"
    
    REM Convert with HandBrake - Choose your preset below:
    
    if %TESTMODE% equ 1 (
        REM TESTING MODE: Show what would be executed
        echo [TESTING] Would run: HandBrakeCLI --input "%%F" --output "!output!" --preset "Very Fast 1080p30" --all-audio --all-subtitles
        echo [TESTING] Would run: HandBrakeCLI --input "%%F" --output "!output!" --preset "Very Fast 1080p30" --all-audio --all-subtitles >> "%logfile%"
    ) else (
        REM ACTUAL CONVERSION MODE
        echo Converting: %%~nxF to !dirname!!counterstr!.mp4
        echo Converting: %%~nxF to !dirname!!counterstr!.mp4 >> "%logfile%"
        
        REM Very fast encoding (larger files, lower quality - good for testing)
        HandBrakeCLI --input "%%F" --output "!output!" --preset "Very Fast 1080p30" --all-audio --all-subtitles
        
        REM Best quality/smallest size (slower encoding)
        REM HandBrakeCLI --input "%%F" --output "!output!" --preset "H.264 MKV 1080p30" --all-audio --all-subtitles
        
        REM Good balance of speed and quality
        REM HandBrakeCLI --input "%%F" --output "!output!" --preset "Fast 1080p30" --all-audio --all-subtitles
        
        REM Other options you can try:
        REM HandBrakeCLI --input "%%F" --output "!output!" --preset "Production Standard" --all-audio --all-subtitles
    )
    
    REM Log end time and result
    echo End time: %date% %time% >> "%logfile%"
    
    if %TESTMODE% equ 1 (
        REM TESTING MODE: Simulate success
        echo [TESTING] SUCCESS (simulated)
        echo SUCCESS (testing mode) >> "%logfile%"
    ) else (
        REM ACTUAL MODE: Check real result
        if !errorlevel! equ 0 (
            echo SUCCESS
            echo SUCCESS >> "%logfile%"
        ) else (
            echo FAILED
            echo FAILED >> "%logfile%"
        )
    )
    echo. >> "%logfile%"
    echo.
)

echo Done! Check the 'converted' folder for your MP4 files.
echo Conversion completed: %date% %time% >> "%logfile%"
echo Check log file: %logfile%
pause
