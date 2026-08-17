import os
import sys
import subprocess
from pathlib import Path

def install_requirements():
    print("Installing requirements...")
    subprocess.check_call([
        sys.executable, "-m", "pip", "install", 
        "exllamav2", "transformers", "soundfile", "accelerate", "huggingface_hub"
    ])

def clone_repos(custom_nodes_path):
    # Match the actual repo folder name
    yue_node_path = custom_nodes_path / "ComfyUI_YuE"
    if not yue_node_path.exists():
        print("Cloning ComfyUI_YuE...")
        # Enable git longpaths locally before cloning
        subprocess.call(["git", "config", "--global", "core.longpaths", "true"])
        subprocess.check_call([
            "git", "clone", 
            "https://github.com/smthemex/ComfyUI_YuE.git", 
            str(yue_node_path)
        ])
    else:
        print("ComfyUI_YuE custom node folder already exists.")

    xcodec_path = yue_node_path / "xcodec_mini_infer"
    if not xcodec_path.exists():
        print("Cloning xcodec_mini_infer...")
        subprocess.check_call([
            "git", "clone", 
            "https://huggingface.co/m-a-p/xcodec_mini_infer", 
            str(xcodec_path)
        ])
    else:
        print("xcodec_mini_infer already exists.")

def download_tokenizer(custom_nodes_path):
    print("Downloading tokenizer...")
    try:
        from huggingface_hub import hf_hub_download
    except ImportError:
        print("huggingface_hub not installed, installing now...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "huggingface_hub"])
        from huggingface_hub import hf_hub_download

    yue_node_path = custom_nodes_path / "ComfyUI_YuE"
    tokenizer_dir = yue_node_path / "mm_tokenizer_v0.2_hf"
    tokenizer_dir.mkdir(parents=True, exist_ok=True)

    # Download tokenizer.model directly to the target folder
    hf_hub_download(
        repo_id="m-a-p/YuE-s1-7B-anneal-en-icl",
        filename="tokenizer.model",
        local_dir=str(tokenizer_dir)
    )
    print("Tokenizer downloaded successfully.")

def main():
    cwd = Path.cwd()
    comfyui_dir = cwd / "ComfyUI_windows_portable" / "ComfyUI"

    if not comfyui_dir.exists():
        comfyui_dir = cwd / "ComfyUI"
        if not comfyui_dir.exists():
            print("ComfyUI directory not found. Creating custom_nodes directory fallback...")
            comfyui_dir.mkdir(parents=True, exist_ok=True)

    custom_nodes_path = comfyui_dir / "custom_nodes"
    custom_nodes_path.mkdir(parents=True, exist_ok=True)

    install_requirements()
    clone_repos(custom_nodes_path)
    download_tokenizer(custom_nodes_path)
    print("\n==========================================")
    print("Setup complete! You can now run the batch file.")
    print("==========================================")

if __name__ == "__main__":
    main()