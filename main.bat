@echo off
setlocal enabledelayedexpansion

:: Create 'resized' folder if it doesn't exist
if not exist "resized" (
    mkdir "resized"
    echo Created folder: resized
)

echo.
echo Starting image compression...

:: Process supported image types
for %%f in (*.jpg *.jpeg *.png *.bmp *.webp *.tiff *.dng *.heic) do (
    echo Processing: %%f
    ffmpeg -hide_banner -loglevel error -i "%%f" -vf scale="if(gt(iw\,ih)\,1920\,-1):if(gt(iw\,ih)\,-1\,1920)" -q:v 4 "resized\%%~nf.jpg"
)

echo.
echo ✅ Done! All resized images are saved in the 'resized' folder.
pause
@echo off
setlocal EnableDelayedExpansion

REM Create folders if not exist
if not exist "LessThan720p" mkdir "LessThan720p"
if not exist "GreaterThan720p" mkdir "GreaterThan720p"

REM Loop through video files
for %%f in (*.mp4 *.mkv *.avi *.mov *.webm) do (
    echo Checking: %%f

    REM Get width
    for /f "delims=" %%w in ('ffprobe -v error -select_streams v:0 -show_entries stream^=width -of default^=noprint_wrappers^=1:nokey^=1 "%%f"') do (
        set /a width=%%w
    )

    REM Get height
    for /f "delims=" %%h in ('ffprobe -v error -select_streams v:0 -show_entries stream^=height -of default^=noprint_wrappers^=1:nokey^=1 "%%f"') do (
        set /a height=%%h
    )

    REM Take the smaller of width and height
    if !width! LSS !height! (
        set /a min=!width!
    ) else (
        set /a min=!height!
    )

    REM Classify based on the smaller dimension
    if !min! LSS 720 (
        echo → Moving "%%f" to LessThan720p [MinRes=!min!]
        move "%%f" "LessThan720p\"
    ) else (
        echo → Moving "%%f" to GreaterThan720p [MinRes=!min!]
        move "%%f" "GreaterThan720p\"
    )
)

echo Done.
pause
@echo off
setlocal enabledelayedexpansion

:: Change to the GreaterThan720p subfolder
if not exist "GreaterThan720p" (
    echo Error: GreaterThan720p folder not found!
    echo Please create the folder and add your videos there.
    pause
    exit /b 1
)

cd "GreaterThan720p"

:: Create output folder if it doesn't exist
if not exist "compressed" (
    mkdir "compressed"
    echo Created folder: compressed
)

echo.
echo Starting compression (max 720p, no upscaling, 128kbps audio)...

for %%f in (*.mp4 *.mov *.avi *.mkv *.webm *.flv *.wmv) do (
    echo Processing: %%f
    ffmpeg -hide_banner -loglevel error -i "%%f" -vf "scale='if(gt(iw,ih),min(iw,1280),-2)':'if(gt(iw,ih),-2,min(ih,1280))',format=yuv420p" -c:v libx264 -crf 28 -preset medium -c:a aac -b:a 128k "compressed\%%~nf.mp4"
)

echo.
echo ✅ Done! Videos saved in the 'GreaterThan720p\compressed' folder.
pause
