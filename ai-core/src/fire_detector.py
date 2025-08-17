"""
Fire Detector Class
Basic fire detection using computer vision techniques
"""

import cv2
import numpy as np
import torch
import torch.nn as nn
import torchvision.transforms as transforms
from PIL import Image
import os

class FireDetector:
    def __init__(self, model_path=None):
        self.model_path = model_path
        self.model = None
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.transforms = self._get_transforms()
        
        # Try to load pre-trained model
        if model_path and os.path.exists(model_path):
            self.load_model(model_path)
        else:
            print("⚠️  Pre-trained model not found, using rule-based detection")
            self.model = None
    
    def _get_transforms(self):
        """Get image preprocessing transforms"""
        return transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                               std=[0.229, 0.224, 0.225])
        ])
    
    def load_model(self, model_path):
        """Load a pre-trained PyTorch model"""
        try:
            self.model = torch.load(model_path, map_location=self.device)
            self.model.eval()
            print(f"✅ Model loaded from {model_path}")
        except Exception as e:
            print(f"❌ Failed to load model: {e}")
            self.model = None
    
    def detect(self, image):
        """
        Main detection method
        Args:
            image: numpy array (RGB format)
        Returns:
            dict with detection results
        """
        if self.model is not None:
            return self._detect_with_ml_model(image)
        else:
            return self._detect_with_cv_rules(image)
    
    def _detect_with_ml_model(self, image):
        """Detection using trained ML model"""
        try:
            # Convert numpy array to PIL Image
            pil_image = Image.fromarray(image)
            
            # Apply transforms
            input_tensor = self.transforms(pil_image).unsqueeze(0).to(self.device)
            
            # Run inference
            with torch.no_grad():
                outputs = self.model(input_tensor)
                probabilities = torch.softmax(outputs, dim=1)
                confidence = probabilities[0][1].item()  # Probability of fire class
                
                fire_detected = confidence > 0.5
                
                # For now, return without bounding boxes (classification only)
                # TODO: Implement object detection for bounding boxes
                return {
                    "fire_detected": fire_detected,
                    "confidence": round(confidence, 3),
                    "bounding_boxes": []  # TODO: Implement object detection
                }
                
        except Exception as e:
            print(f"❌ ML model detection failed: {e}")
            # Fallback to rule-based detection
            return self._detect_with_cv_rules(image)
    
    def _detect_with_cv_rules(self, image):
        """
        Rule-based fire detection using computer vision
        This is a simple approach for demonstration
        """
        try:
            # Convert to HSV for better color detection
            hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
            
            # Define fire color ranges in HSV
            # Orange/Red colors typical of fire
            lower_fire1 = np.array([0, 50, 50])    # Lower red
            upper_fire1 = np.array([10, 255, 255])
            
            lower_fire2 = np.array([170, 50, 50])  # Upper red
            upper_fire2 = np.array([180, 255, 255])
            
            # Orange colors
            lower_orange = np.array([10, 50, 50])
            upper_orange = np.array([25, 255, 255])
            
            # Create masks
            mask1 = cv2.inRange(hsv, lower_fire1, upper_fire1)
            mask2 = cv2.inRange(hsv, lower_fire2, upper_fire2)
            mask3 = cv2.inRange(hsv, lower_orange, upper_orange)
            
            # Combine masks
            fire_mask = cv2.bitwise_or(mask1, mask2)
            fire_mask = cv2.bitwise_or(fire_mask, mask3)
            
            # Remove noise
            kernel = np.ones((3,3), np.uint8)
            fire_mask = cv2.morphologyEx(fire_mask, cv2.MORPH_CLOSE, kernel)
            fire_mask = cv2.morphologyEx(fire_mask, cv2.MORPH_OPEN, kernel)
            
            # Find contours
            contours, _ = cv2.findContours(fire_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Calculate fire area percentage
            total_pixels = image.shape[0] * image.shape[1]
            fire_pixels = cv2.countNonZero(fire_mask)
            fire_percentage = fire_pixels / total_pixels
            
            # Determine if fire is detected
            fire_detected = fire_percentage > 0.01  # At least 1% of image
            confidence = min(fire_percentage * 10, 0.95)  # Scale confidence
            
            # Get bounding boxes for significant contours
            bounding_boxes = []
            min_area = 500  # Minimum area for a fire region
            
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > min_area:
                    x, y, w, h = cv2.boundingRect(contour)
                    box_confidence = min(area / (image.shape[0] * image.shape[1]) * 20, 0.95)
                    
                    bounding_boxes.append({
                        "x": int(x),
                        "y": int(y),
                        "width": int(w),
                        "height": int(h),
                        "confidence": round(box_confidence, 3),
                        "class": "fire"
                    })
            
            return {
                "fire_detected": fire_detected,
                "confidence": round(confidence, 3),
                "bounding_boxes": bounding_boxes
            }
            
        except Exception as e:
            print(f"❌ CV rule-based detection failed: {e}")
            # Return safe default
            return {
                "fire_detected": False,
                "confidence": 0.0,
                "bounding_boxes": []
            }
