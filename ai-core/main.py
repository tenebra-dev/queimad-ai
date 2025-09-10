#!/usr/bin/env python3
"""
🔥 Fire Detection - Main Entry Point
Quick access to YOLOv8 fire detection system
"""

import sys
import os
import subprocess
from pathlib import Path

def check_dataset_status():
    """Check dataset extraction status"""
    dataset_zip = Path("datasets/wildfire.v10-origin.yolov8.zip")
    dataset_extracted = Path("datasets/wildfire/data.yaml")
    
    print("📊 Dataset Status Check:")
    print(f"   ZIP file: {'✅ Found' if dataset_zip.exists() else '❌ Missing'}")
    print(f"   Extracted: {'✅ Found' if dataset_extracted.exists() else '❌ Missing'}")
    
    if dataset_zip.exists() and not dataset_extracted.exists():
        print("\n💡 Dataset ZIP encontrado mas não extraído!")
        print("Execute:")
        if os.name == 'nt':  # Windows
            print("   cd datasets")
            print("   Expand-Archive -Path 'wildfire.v10-origin.yolov8.zip' -DestinationPath '.'")
        else:  # Linux/macOS
            print("   cd datasets && unzip wildfire.v10-origin.yolov8.zip")
    elif not dataset_zip.exists():
        print("\n💡 Dataset não encontrado!")
        print("1. Baixe de: https://universe.roboflow.com/test0-sbyyu/wildfire-soeq8/dataset/10")
        print("2. Formato: YOLOv8")
        print("3. Salve como: datasets/wildfire.v10-origin.yolov8.zip")
        print("4. Execute extração conforme README.md")
    
    return dataset_extracted.exists()

def check_model_exists():
    """Check if trained model exists"""
    model_paths = [
        "runs/detect/fire_detection_yolo/weights/best.pt",
        "runs/detect/fire_detection_colab/weights/best.pt", 
        "runs/detect/fire_detection_colab_v2/weights/best.pt",
        "models/trained/best.pt"
    ]
    
    for path in model_paths:
        if Path(path).exists():
            return path
    return None
    """Check if trained model exists"""
    model_paths = [
        "runs/detect/fire_detection_yolo/weights/best.pt",
        "runs/detect/fire_detection_colab/weights/best.pt", 
        "runs/detect/fire_detection_colab_v2/weights/best.pt",
        "models/trained/best.pt"
    ]
    
    for path in model_paths:
        if Path(path).exists():
            return path
    return None

def run_command_safely(command, description):
    """Run command and handle errors gracefully"""
    print(f"🚀 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=False, capture_output=False, text=True)
        if result.returncode != 0:
            print(f"⚠️  {description} finished with warnings")
            input("Press Enter to continue...")
        return True
    except Exception as e:
        print(f"❌ {description} failed: {e}")
        print(f"💡 Try running manually: {command}")
        input("Press Enter to continue...")
        return False

def main():
    """Main entry point with menu"""
    
    print("🔥 Fire Detection AI - YOLOv8")
    print("=" * 40)
    
    # Check if model exists
    model_path = check_model_exists()
    if model_path:
        print(f"✅ Modelo treinado encontrado: {model_path}")
    else:
        print("⚠️  Nenhum modelo treinado encontrado")
        print("💡 Recomendação: Treinar modelo primeiro (opção 1)")
    
    # Check dataset status
    dataset_ok = check_dataset_status()
    if not dataset_ok:
        print("⚠️  Dataset não extraído - veja instruções no README.md")
    
    print()
    print("Choose an option:")
    print("1. 🏋️  Train YOLOv8 model")
    print("2. 🧪 Test trained model")
    print("3. 📚 Legacy MobileNetV2 (test)")
    print("4. 📚 Legacy MobileNetV2 (train)") 
    print("5. 📓 Open Google Colab notebook")
    print("6. ⚙️  Run setup")
    print("7. 📊 Check dataset & model status")
    print("8. 📁 Show project structure")
    print("9. 🚪 Exit")
    
    while True:
        try:
            choice = input(f"\nEnter choice (1-9): ").strip()
            
            if choice == "1":
                if not check_dataset_status():
                    print("❌ Dataset não encontrado! Extraia o dataset primeiro.")
                    continue
                print("🚀 Starting YOLOv8 training...")
                if not run_command_safely("poetry run python src/yolo_fire_detection.py", "YOLOv8 Training"):
                    print("💡 Try running setup first (option 6)")
                break
                
            elif choice == "2":
                if not model_path:
                    print("❌ No trained model found!")
                    print("💡 Please train a model first (option 1) or use Google Colab (option 5)")
                    continue
                    
                print("🧪 Testing YOLOv8 model...")
                run_command_safely("poetry run python src/test_trained_model.py", "YOLOv8 Testing")
                break
                
            elif choice == "3":
                print("📚 Testing legacy MobileNetV2...")
                run_command_safely("poetry run python legacy/test_model.py", "Legacy Testing")
                break
                
            elif choice == "4":
                print("📚 Training legacy MobileNetV2...")
                run_command_safely("poetry run python legacy/quick_train.py", "Legacy Training")
                break
                
            elif choice == "5":
                notebook_path = Path("notebooks/googlecolab_model_training.md")
                if notebook_path.exists():
                    print(f"📓 Opening {notebook_path}")
                    print("💡 Copy the content to Google Colab for FREE GPU training!")
                    try:
                        if os.name == 'nt':  # Windows
                            os.system(f'start "" "{notebook_path}"')
                        elif os.name == 'posix':  # macOS/Linux
                            os.system(f'open "{notebook_path}"')
                    except:
                        print(f"📁 Please open manually: {notebook_path}")
                else:
                    print("❌ Notebook not found!")
                break
                
            elif choice == "6":
                print("⚙️  Running setup...")
                run_command_safely("poetry run python setup.py", "Project Setup")
                break
                
            elif choice == "7":
                print("📊 System Status Check:")
                check_dataset_status()
                model_path_fresh = check_model_exists()
                print(f"   Trained model: {'✅ Found at ' + model_path_fresh if model_path_fresh else '❌ Not found'}")
                continue
                
            elif choice == "8":
                print("📊 Project Structure:")
                print("""
📁 AI-Core Project Structure:
├── 🎯 main.py              (START HERE - This menu)
├── ⚙️  setup.py            (One-time setup)
├── 🔧 config.py           (Configuration)
├── 📦 pyproject.toml       (Dependencies)
│
├── 🔥 src/                 (YOLOv8 - Current Model)
│   ├── yolo_fire_detection.py  (Training)
│   └── test_trained_model.py   (Testing)
│
├── 📚 legacy/              (MobileNetV2 - Old Model)
│   ├── quick_train.py          (Training)
│   └── test_model.py           (Testing)
│
├── 📓 notebooks/           (Google Colab Tutorial)
│   └── googlecolab_model_training.md
│
└── 📁 Data & Models
    ├── datasets/wildfire/      (Training data - EXTRACT FIRST!)
    ├── models/trained/         (Saved models)
    └── runs/detect/           (Training results)
                """)
                continue
                
            elif choice == "9":
                print("👋 Goodbye!")
                break
                
            else:
                print("❌ Invalid choice. Please enter 1-9.")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
