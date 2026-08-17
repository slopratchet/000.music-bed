@echo off
setlocal enabledelayedexpansion

echo ===================================================
echo   ComfyUI-YuE Low-VRAM Local Automation Setup
echo ===================================================

:: Check if ComfyUI_windows_portable exists
if not exist "ComfyUI_windows_portable\" (
    echo [INFO] ComfyUI_windows_portable not found in the current directory.
    echo [INFO] Downloading the official ComfyUI Windows Portable release...
    curl -L -o ComfyUI_windows_portable_nvidia_cu121_or_cpu.7z https://github.com/comfyanonymous/ComfyUI/releases/latest/download/ComfyUI_windows_portable_nvidia_cu121_or_cpu.7z

    echo [INFO] Extracting ComfyUI Windows Portable release...
    :: Use tar on newer Windows 11 which supports 7z natively, or fallback to powershell/manual
    tar -xf ComfyUI_windows_portable_nvidia_cu121_or_cpu.7z
    if errorlevel 1 (
        echo [ERROR] Native extraction failed. Attempting to use 7z.exe if installed...
        7z x ComfyUI_windows_portable_nvidia_cu121_or_cpu.7z
        if errorlevel 1 (
            echo [ERROR] Extraction failed. Please install 7-Zip or extract ComfyUI_windows_portable_nvidia_cu121_or_cpu.7z manually.
            pause
            exit /b 1
        )
    )

    if not exist "ComfyUI_windows_portable\" (
        echo [ERROR] Extraction completed but ComfyUI_windows_portable folder not found.
        pause
        exit /b 1
    )
)

:: Ensure embedded python exists
if not exist "ComfyUI_windows_portable\python_embeded\python.exe" (
    echo [ERROR] Cannot find embedded Python: ComfyUI_windows_portable\python_embeded\python.exe
    pause
    exit /b 1
)

echo [INFO] Running ComfyUI-YuE Setup Script...
"ComfyUI_windows_portable\python_embeded\python.exe" scripts\setup_comfy_yue.py
if %errorlevel% neq 0 (
    echo [ERROR] Setup script failed.
    pause
    exit /b %errorlevel%
)

:: Verify model directories exist (or warn if not)
if not exist "ComfyUI_windows_portable\ComfyUI\models\yue\" (
    echo [WARNING] No 'yue' model directory found in ComfyUI\models\
    echo Make sure you place YuE-s1-7B-anneal-en-exl2 and YuE-s2-1B-general-exl2 inside ComfyUI_windows_portable\ComfyUI\models\yue\
)

echo [INFO] Launching ComfyUI with Low-VRAM settings...
cd ComfyUI_windows_portable
.\python_embeded\python.exe -s ComfyUI\main.py --lowvram --preview-method auto

pause
