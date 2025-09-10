"""
🔥 Fire Detection with YOLOv8 using Roboflow Dataset
Advanced fire detection with bounding box localization
"""

import os
import sys
from pathlib import Path
import torch
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import requests
import zipfile
import yaml
from datetime import datetime

# Install required packages if not present
try:
    from ultralytics import YOLO
    import roboflow
except ImportError:
    print("📦 Installing required packages...")
    os.system("pip install ultralytics roboflow")
    from ultralytics import YOLO
    import roboflow

class FireDetectionYOLO:
    def __init__(self):
        self.model = None
        self.dataset_path = None
        self.trained_model_path = None
        
    def setup_roboflow_dataset(self, api_key=None):
        """
        Setup Roboflow dataset via API
        Get your API key from: https://app.roboflow.com/settings/api
        """
        
        print("🔥 Setting up Roboflow Wildfire Dataset")
        print("=" * 50)
        
        if api_key is None:
            print("📝 To use Roboflow API, you need an API key:")
            print("1. Go to https://app.roboflow.com/settings/api")
            print("2. Copy your API key")
            print("3. Set it as environment variable: ROBOFLOW_API_KEY")
            print("4. Or pass it as parameter to this function")
            
            # Check environment variable
            api_key = os.getenv('ROBOFLOW_API_KEY')
            if not api_key:
                print("\n⚠️  No API key found. Using manual download method...")
                return self.manual_dataset_setup()
        
        try:
            # Initialize Roboflow
            rf = roboflow.Roboflow(api_key=api_key)
            
            # Access the wildfire project
            project = rf.workspace("test0-sbyyu").project("wildfire-soeq8")
            dataset = project.version(10).download("yolov8")
            
            self.dataset_path = dataset.location
            print(f"✅ Dataset downloaded to: {self.dataset_path}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error downloading via API: {e}")
            print("🔄 Falling back to manual setup...")
            return self.manual_dataset_setup()
    
    def manual_dataset_setup(self):
        """
        Manual dataset setup instructions
        """
        print("\n📋 MANUAL DATASET SETUP INSTRUCTIONS")
        print("=" * 50)
        print("1. Go to: https://universe.roboflow.com/test0-sbyyu/wildfire-soeq8/dataset/10")
        print("2. Click 'Download' button")
        print("3. Choose 'YOLOv8' format")
        print("4. Download and extract to: ai-core/datasets/wildfire/")
        print("5. Run this script again")
        
        # Check if dataset exists locally
        local_dataset_path = "datasets/wildfire"
        if os.path.exists(local_dataset_path):
            print(f"\n✅ Found local dataset at: {local_dataset_path}")
            self.dataset_path = local_dataset_path
            return True
        else:
            print(f"\n❌ Dataset not found at: {local_dataset_path}")
            return False
    
    def validate_dataset(self):
        """Validate dataset structure"""
        if not self.dataset_path:
            return False
            
        required_files = [
            'data.yaml',
            'train/images',
            'train/labels', 
            'valid/images',
            'valid/labels'
        ]
        
        print(f"\n🔍 Validating dataset structure...")
        for file_path in required_files:
            full_path = os.path.join(self.dataset_path, file_path)
            if os.path.exists(full_path):
                if os.path.isdir(full_path):
                    count = len(os.listdir(full_path))
                    print(f"✅ {file_path}: {count} files")
                else:
                    print(f"✅ {file_path}: exists")
            else:
                print(f"❌ {file_path}: missing")
                return False
        
        # Check data.yaml content
        yaml_path = os.path.join(self.dataset_path, 'data.yaml')
        try:
            with open(yaml_path, 'r') as f:
                data_config = yaml.safe_load(f)
                print(f"\n📄 Dataset configuration:")
                print(f"   Classes: {data_config.get('nc', 'unknown')}")
                print(f"   Names: {data_config.get('names', 'unknown')}")
        except Exception as e:
            print(f"⚠️  Could not read data.yaml: {e}")
        
        return True
    
    def train_model(self, epochs=100, img_size=640, batch_size=16):
        """Train YOLOv8 model with the wildfire dataset"""
        
        # Auto-detect local dataset if not setup via API
        if not self.dataset_path:
            local_dataset = "datasets/wildfire"
            if os.path.exists(local_dataset) and os.path.exists(os.path.join(local_dataset, "data.yaml")):
                print(f"✅ Found local dataset at: {local_dataset}")
                self.dataset_path = local_dataset
            else:
                print("❌ Dataset not setup. Run setup_roboflow_dataset() first")
                return False
            
        if not self.validate_dataset():
            print("❌ Dataset validation failed")
            return False
        
        print(f"\n🚀 Starting YOLOv8 Training")
        print("=" * 50)
        
        # Initialize YOLOv8 model
        model = YOLO('yolov8n.pt')  # nano version - fastest
        # Alternative options:
        # model = YOLO('yolov8s.pt')  # small - balanced
        # model = YOLO('yolov8m.pt')  # medium - more accurate
        
        # Setup training parameters
        data_yaml = os.path.join(self.dataset_path, 'data.yaml')
        
        print(f"📊 Training Parameters:")
        print(f"   Model: YOLOv8n (nano)")
        print(f"   Dataset: {data_yaml}")
        print(f"   Epochs: {epochs}")
        print(f"   Image size: {img_size}")
        print(f"   Batch size: {batch_size}")
        print(f"   Device: {'GPU' if torch.cuda.is_available() else 'CPU'}")
        
        try:
            # Start training
            results = model.train(
                data=data_yaml,
                epochs=epochs,
                imgsz=img_size,
                batch=batch_size,
                name='fire_detection_yolo',
                project='runs/detect',
                
                # Optimization settings
                patience=15,      # Early stopping patience
                save_period=10,   # Save checkpoint every 10 epochs
                
                # Data augmentation for fire detection
                hsv_h=0.015,     # Hue variation (important for fire colors)
                hsv_s=0.7,       # Saturation variation
                hsv_v=0.4,       # Value/brightness variation
                degrees=10,      # Rotation augmentation
                translate=0.1,   # Translation augmentation
                scale=0.5,       # Scale augmentation
                fliplr=0.5,      # Horizontal flip
                
                # Learning rate settings
                lr0=0.01,        # Initial learning rate
                lrf=0.1,         # Final learning rate factor
                momentum=0.937,  # SGD momentum
                weight_decay=0.0005,  # Weight decay
                
                # Hardware settings
                device=0 if torch.cuda.is_available() else 'cpu',
                workers=8 if torch.cuda.is_available() else 4,
                
                # Validation settings
                val=True,        # Validate during training
                plots=True,      # Generate training plots
                save_json=True,  # Save results in JSON format
            )
            
            # Save trained model path
            self.trained_model_path = f"runs/detect/fire_detection_yolo/weights/best.pt"
            
            print(f"\n✅ Training completed!")
            print(f"📊 Best model saved to: {self.trained_model_path}")
            
            # Display training results
            print(f"\n📈 Training Results:")
            metrics = results.results_dict
            if metrics:
                print(f"   mAP50: {metrics.get('metrics/mAP50(B)', 'N/A'):.3f}")
                print(f"   mAP50-95: {metrics.get('metrics/mAP50-95(B)', 'N/A'):.3f}")
                print(f"   Precision: {metrics.get('metrics/precision(B)', 'N/A'):.3f}")
                print(f"   Recall: {metrics.get('metrics/recall(B)', 'N/A'):.3f}")
            
            return True
            
        except Exception as e:
            print(f"❌ Training failed: {e}")
            return False
    
    def load_trained_model(self, model_path=None):
        """Load trained YOLO model"""
        
        if model_path is None:
            model_path = self.trained_model_path or "runs/detect/fire_detection_yolo/weights/best.pt"
        
        if not os.path.exists(model_path):
            print(f"❌ Model not found: {model_path}")
            print("🔄 Train the model first using train_model()")
            return False
        
        try:
            self.model = YOLO(model_path)
            print(f"✅ Model loaded from: {model_path}")
            return True
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            return False
    
    def detect_fire(self, image_path, conf_threshold=0.5):
        """
        Detect fire in an image with bounding boxes
        Returns detection results with coordinates
        """
        
        if self.model is None:
            print("❌ Model not loaded. Use load_trained_model() first")
            return None
        
        try:
            # Run detection
            results = self.model(image_path, conf=conf_threshold)
            
            detections = []
            
            for r in results:
                boxes = r.boxes
                
                if boxes is not None:
                    for box in boxes:
                        # Extract box information
                        x1, y1, x2, y2 = box.xyxy[0].tolist()
                        confidence = box.conf[0].item()
                        class_id = int(box.cls[0].item())
                        
                        # Get class name
                        class_names = self.model.names
                        class_name = class_names[class_id]
                        
                        detection = {
                            'class': class_name,
                            'confidence': confidence,
                            'bbox': [int(x1), int(y1), int(x2), int(y2)],
                            'center': [int((x1+x2)/2), int((y1+y2)/2)],
                            'area': int((x2-x1) * (y2-y1))
                        }
                        
                        detections.append(detection)
            
            return detections
            
        except Exception as e:
            print(f"❌ Detection error: {e}")
            return None
    
    def visualize_detections(self, image_path, detections, save_path=None):
        """
        Visualize detections on image with bounding boxes
        """
        
        # Load image
        image = cv2.imread(image_path)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Define colors for different classes
        colors = {
            'fire': (255, 0, 0),      # Red
            'smoke': (255, 165, 0),   # Orange
            'wildfire': (255, 0, 0),  # Red
        }
        
        # Draw detections
        for detection in detections:
            x1, y1, x2, y2 = detection['bbox']
            class_name = detection['class']
            confidence = detection['confidence']
            
            # Get color for class
            color = colors.get(class_name.lower(), (0, 255, 0))  # Default green
            
            # Draw bounding box
            cv2.rectangle(image_rgb, (x1, y1), (x2, y2), color, 3)
            
            # Draw label
            label = f"{class_name}: {confidence:.2f}"
            label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)[0]
            
            # Background for text
            cv2.rectangle(image_rgb, (x1, y1-label_size[1]-10), 
                         (x1+label_size[0], y1), color, -1)
            
            # Text
            cv2.putText(image_rgb, label, (x1, y1-5), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Display results
        plt.figure(figsize=(12, 8))
        plt.imshow(image_rgb)
        plt.axis('off')
        plt.title(f'Fire Detection Results - {len(detections)} detections found')
        
        # Save if requested
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            print(f"📸 Results saved to: {save_path}")
        
        plt.show()
        
        return image_rgb
    
    def test_model_performance(self, test_images_dir=None):
        """
        Test model performance on test dataset or custom images
        """
        
        if self.model is None:
            print("❌ Model not loaded")
            return
        
        # Auto-detect dataset path if not provided
        if test_images_dir is None:
            if not self.dataset_path:
                local_dataset = "datasets/wildfire"
                if os.path.exists(local_dataset):
                    self.dataset_path = local_dataset
            
            if self.dataset_path:
                test_images_dir = os.path.join(self.dataset_path, 'test/images')
        
        if not test_images_dir or not os.path.exists(test_images_dir):
            print(f"❌ Test images directory not found: {test_images_dir}")
            return
        
        print(f"🧪 Testing model performance...")
        print(f"📁 Test directory: {test_images_dir}")
        
        # Get test images
        test_images = [f for f in os.listdir(test_images_dir) 
                      if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        
        print(f"📊 Found {len(test_images)} test images")
        
        total_detections = 0
        images_with_detections = 0
        
        # Test first 10 images as sample
        sample_images = test_images[:10]
        
        for img_name in sample_images:
            img_path = os.path.join(test_images_dir, img_name)
            detections = self.detect_fire(img_path, conf_threshold=0.5)
            
            if detections:
                total_detections += len(detections)
                images_with_detections += 1
                
                print(f"📸 {img_name}: {len(detections)} detections")
                for det in detections:
                    print(f"   - {det['class']}: {det['confidence']:.3f}")
            else:
                print(f"📸 {img_name}: No detections")
        
        print(f"\n📊 Sample Test Results:")
        print(f"   Images tested: {len(sample_images)}")
        print(f"   Images with detections: {images_with_detections}")
        print(f"   Total detections: {total_detections}")
        print(f"   Average detections per image: {total_detections/len(sample_images):.1f}")
    
    def create_web_api_demo(self):
        """
        Create a simple web demo using Streamlit
        """
        
        demo_code = '''
import streamlit as st
from yolo_fire_detection import FireDetectionYOLO
from PIL import Image
import tempfile
import os

st.title("🔥 Fire Detection with YOLOv8")
st.write("Upload an image to detect fire and smoke with precise bounding boxes")

# Initialize detector
@st.cache_resource
def load_model():
    detector = FireDetectionYOLO()
    if detector.load_trained_model():
        return detector
    else:
        st.error("Model not found! Train the model first.")
        return None

detector = load_model()

if detector:
    # File uploader
    uploaded_file = st.file_uploader("Choose an image...", type=['jpg', 'jpeg', 'png'])
    
    if uploaded_file is not None:
        # Display original image
        image = Image.open(uploaded_file)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Original Image")
            st.image(image, use_column_width=True)
        
        # Confidence threshold slider
        conf_threshold = st.slider("Confidence Threshold", 0.1, 1.0, 0.5, 0.1)
        
        if st.button("🔍 Detect Fire", type="primary"):
            with st.spinner("Analyzing image..."):
                # Save uploaded file temporarily
                with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
                    image.save(tmp_file.name)
                    
                    # Run detection
                    detections = detector.detect_fire(tmp_file.name, conf_threshold)
                    
                    with col2:
                        st.subheader("Detection Results")
                        
                        if detections:
                            # Visualize results
                            result_img = detector.visualize_detections(
                                tmp_file.name, detections, save_path=None
                            )
                            st.image(result_img, use_column_width=True)
                            
                            # Show detection details
                            st.write("### Detections Found:")
                            for i, det in enumerate(detections):
                                st.write(f"**{i+1}. {det['class'].title()}**")
                                st.write(f"   - Confidence: {det['confidence']:.3f}")
                                st.write(f"   - Position: ({det['bbox'][0]}, {det['bbox'][1]}) to ({det['bbox'][2]}, {det['bbox'][3]})")
                                st.write(f"   - Area: {det['area']} pixels")
                                
                            # Summary
                            fire_count = sum(1 for d in detections if 'fire' in d['class'].lower())
                            smoke_count = sum(1 for d in detections if 'smoke' in d['class'].lower())
                            
                            if fire_count > 0:
                                st.error(f"🚨 FIRE DETECTED! {fire_count} fire region(s) found")
                            if smoke_count > 0:
                                st.warning(f"💨 SMOKE DETECTED! {smoke_count} smoke region(s) found")
                        else:
                            st.image(image, use_column_width=True)
                            st.success("✅ No fire or smoke detected")
                    
                    # Cleanup
                    os.unlink(tmp_file.name)
'''
        
        # Save demo file
        with open('streamlit_fire_demo.py', 'w') as f:
            f.write(demo_code)
        
        print("📱 Web demo created: streamlit_fire_demo.py")
        print("🚀 Run with: streamlit run streamlit_fire_demo.py")


def main():
    """Main execution function"""
    
    print("🔥 YOLOv8 Fire Detection Setup")
    print("=" * 50)
    
    # Initialize detector
    detector = FireDetectionYOLO()
    
    # Menu
    print("\nChoose an option:")
    print("1. Setup dataset from Roboflow")
    print("2. Train YOLOv8 model")
    print("3. Test trained model")
    print("4. Create web demo")
    print("5. Full pipeline (setup + train + test)")
    
    choice = input("\nEnter your choice (1-5): ").strip()
    
    if choice == "1":
        # Setup dataset
        api_key = input("Enter Roboflow API key (or press Enter to skip): ").strip()
        if not api_key:
            api_key = None
        
        if detector.setup_roboflow_dataset(api_key):
            print("✅ Dataset setup completed!")
        else:
            print("❌ Dataset setup failed")
    
    elif choice == "2":
        # Train model
        epochs = int(input("Enter number of epochs (default 100): ") or "100")
        
        print("📊 Available model sizes:")
        print("n = nano (fastest, least accurate)")
        print("s = small (balanced)")
        print("m = medium (slower, more accurate)")
        
        if detector.train_model(epochs=epochs):
            print("✅ Training completed!")
        else:
            print("❌ Training failed")
    
    elif choice == "3":
        # Test model
        if detector.load_trained_model():
            detector.test_model_performance()
        else:
            print("❌ Could not load model")
    
    elif choice == "4":
        # Create web demo
        detector.create_web_api_demo()
    
    elif choice == "5":
        # Full pipeline
        print("🚀 Starting full pipeline...")
        
        # 1. Setup dataset
        if detector.setup_roboflow_dataset():
            print("✅ Step 1: Dataset setup completed")
            
            # 2. Train model
            if detector.train_model(epochs=50):  # Reduced epochs for demo
                print("✅ Step 2: Training completed")
                
                # 3. Test model
                if detector.load_trained_model():
                    print("✅ Step 3: Model loaded")
                    detector.test_model_performance()
                    
                    # 4. Create demo
                    detector.create_web_api_demo()
                    print("✅ Step 4: Web demo created")
                    
                    print("\n🎉 Full pipeline completed successfully!")
                else:
                    print("❌ Step 3 failed: Could not load model")
            else:
                print("❌ Step 2 failed: Training failed")
        else:
            print("❌ Step 1 failed: Dataset setup failed")
    
    else:
        print("❌ Invalid choice")


if __name__ == "__main__":
    main()
