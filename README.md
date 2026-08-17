# Self-Contained ComfyUI-YuE Local Automation

This repository provides a local execution environment for YuE (Music Generation LLM) designed specifically for hardware with limited system RAM and VRAM. It leverages the official ComfyUI Windows Portable release to bypass system Python mismatches and provide isolated package management.

## Prerequisites
- Windows OS (due to `.bat` launcher and ComfyUI portable)
- Hardware with decent RAM/VRAM, though optimizations are built-in for low-VRAM configurations.

## Setup Instructions

1. **Download ComfyUI Portable**
   Download the official ComfyUI Windows Portable release from the [ComfyUI GitHub Releases page](https://github.com/comfyanonymous/ComfyUI/releases).
   Extract it directly into the root folder of this repository so that a folder named `ComfyUI_windows_portable` is present next to `run_yue_comfy.bat`.

2. **Download EXL2 Models Manually**
   Due to size constraints, you need to manually download the quantized EXL2 models.
   - Stage 1 (EXL2): Download the `YuE-s1-7B-anneal-en-exl2` model and place it in `ComfyUI_windows_portable/ComfyUI/models/yue/YuE-s1-7B-anneal-en-exl2`.
   - Stage 2 (EXL2): Download the `YuE-s2-1B-general-exl2` model and place it in `ComfyUI_windows_portable/ComfyUI/models/yue/YuE-s2-1B-general-exl2`.

3. **Input Audio Prompt**
   Place your input conditioning audio file named `000.wav` into the `ComfyUI_windows_portable/ComfyUI/input` folder. (Create the folder if it does not exist).

4. **Launch**
   Double-click `run_yue_comfy.bat`.

   The script will:
   - Use the isolated Python environment within `ComfyUI_windows_portable`.
   - Install required dependencies automatically (e.g., `exllamav2`, `transformers`, `accelerate`).
   - Clone necessary custom nodes (`ComfyUI-YuE` and `xcodec_mini_infer`).
   - Download the tokenizer automatically.
   - Launch ComfyUI with `--lowvram` and `--preview-method auto` arguments.

## Using the Workflow
Load `workflows/yue_low_vram_template.json` from the ComfyUI web interface. It comes pre-configured with Stage 1 CPU offloading and batch sizes adjusted for stability on lower VRAM systems. Adjust your prompts within the loaded nodes as necessary. Outputs will be saved to `ComfyUI_windows_portable/ComfyUI/output`.
