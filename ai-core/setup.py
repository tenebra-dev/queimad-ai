#!/usr/bin/env python3
"""
🔥 Fire Detection Setup Script
Quick setup for the YOLOv8 fire detection system
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """Run a command and show progress"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_dependencies():
    """Check if required tools are installed"""
    print("🔍 Checking dependencies...")
    
    # Check Python version
    if sys.version_info < (3, 11):
        print(f"❌ Python 3.11+ required. Current: {sys.version}")
        return False
    print(f"✅ Python {sys.version.split()[0]}")
    
    # Check Poetry
    try:
        result = subprocess.run("poetry --version", shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {result.stdout.strip()}")
        else:
            print("❌ Poetry not found. Install from: https://python-poetry.org/")
            return False
    except:
        print("❌ Poetry not found. Install from: https://python-poetry.org/")
        return False
    
    return True

def setup_project():
    """Setup the project"""
    print("🚀 Setting up Fire Detection AI Core...")
    
    if not check_dependencies():
        return False
    
    # Install dependencies
    print("🔄 Updating Poetry lock file...")
    if not run_command("poetry lock", "Updating Poetry dependencies"):
        print("⚠️  Lock update failed, trying alternative...")
        if not run_command("poetry install --no-cache", "Installing Python dependencies (no cache)"):
            return False
    else:
        if not run_command("poetry install", "Installing Python dependencies"):
            return False
    
    # Create required directories
    directories = [
        "datasets",
        "models/checkpoints",
        "models/trained",
        "runs/detect",
        "logs"
    ]
    
    for directory in directories:
        dir_path = Path(directory)
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"📁 Created directory: {directory}")
    
    # Download YOLOv8 base model if not exists
    yolo_model = Path("yolov8n.pt")
    if not yolo_model.exists():
        print("📥 Downloading YOLOv8 base model...")
        try:
            import urllib.request
            urllib.request.urlretrieve(
                "https://github.com/ultralytics/assets/releases/download/v8.2.0/yolov8n.pt",
                "yolov8n.pt"
            )
            print("✅ YOLOv8 model downloaded")
        except Exception as e:
            print(f"⚠️  Could not download YOLOv8 model: {e}")
            print("You can download it manually or it will be downloaded automatically during first use")
    
    # Check dataset
    dataset_zip = Path("datasets/wildfire.v10-origin.yolov8.zip")
    dataset_extracted = Path("datasets/wildfire/data.yaml")
    
    if dataset_zip.exists() and not dataset_extracted.exists():
        print("📦 Dataset ZIP encontrado, mas não extraído")
        print("💡 Execute manualmente:")
        if os.name == 'nt':  # Windows
            print("   cd datasets && Expand-Archive -Path 'wildfire.v10-origin.yolov8.zip' -DestinationPath '.'")
        else:  # Linux/macOS
            print("   cd datasets && unzip wildfire.v10-origin.yolov8.zip")
        print("   Ou veja instruções no README.md")
    elif dataset_extracted.exists():
        print("✅ Dataset YOLOv8 encontrado e extraído")
    else:
        print("⚠️  Dataset não encontrado")
        print("💡 Baixe de: https://universe.roboflow.com/test0-sbyyu/wildfire-soeq8/dataset/10")
        print("   Formato: YOLOv8, salvar como: datasets/wildfire.v10-origin.yolov8.zip")
        print("   Depois extrair conforme README.md")
    
    print("\n🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Run: poetry run python main.py")
    print("2. Or train model: poetry run python src/yolo_fire_detection.py")
    print("3. Or test model: poetry run python src/test_trained_model.py")
    print("4. For Google Colab: see notebooks/googlecolab_model_training.md")
    
    return True

def main():
    """Main setup function"""
    print("🔥 Fire Detection AI - Setup")
    print("=" * 40)
    
    if setup_project():
        print("\n✅ All done! Your fire detection system is ready.")
    else:
        print("\n❌ Setup failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
