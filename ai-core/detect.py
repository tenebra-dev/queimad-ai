"""
QueimadAI - Fire Detection Script
Main detection script that can be called from the Node.js API
"""

import sys
import json
import time
import os
from pathlib import Path
import cv2
import numpy as np
from PIL import Image
import torch
import torchvision.transforms as transforms

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from fire_detector import FireDetector
from video_processor import VideoProcessor

def main():
    if len(sys.argv) < 3:
        print(json.dumps({
            "error": "Usage: python detect.py <image|video> <file_path>",
            "success": False
        }))
        sys.exit(1)
    
    detection_type = sys.argv[1]
    file_path = sys.argv[2]
    
    if not os.path.exists(file_path):
        print(json.dumps({
            "error": f"File not found: {file_path}",
            "success": False
        }))
        sys.exit(1)
    
    try:
        # Initialize detector
        detector = FireDetector()
        
        start_time = time.time()
        
        if detection_type == "image":
            result = detect_image(detector, file_path)
        elif detection_type == "video":
            result = detect_video(detector, file_path)
        else:
            raise ValueError(f"Invalid detection type: {detection_type}")
        
        # Add processing time
        processing_time = time.time() - start_time
        result["metadata"]["processing_time"] = f"{processing_time:.1f}s"
        
        # Output result as JSON
        print(json.dumps(result, indent=2))
        
    except Exception as e:
        print(json.dumps({
            "error": str(e),
            "success": False
        }))
        sys.exit(1)

def detect_image(detector, image_path):
    """Detect fire in a single image"""
    # Load image
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Could not load image: {image_path}")
    
    # Convert BGR to RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Detect fire
    result = detector.detect(image_rgb)
    
    # Get image dimensions
    height, width = image.shape[:2]
    
    return {
        "fire_detected": result["fire_detected"],
        "confidence": result["confidence"],
        "bounding_boxes": result["bounding_boxes"],
        "metadata": {
            "model_version": "v1.0.0",
            "image_size": f"{width}x{height}",
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "processing_time": "0.0s"  # Will be updated in main()
        }
    }

def detect_video(detector, video_path):
    """Detect fire in video frames"""
    processor = VideoProcessor(detector)
    result = processor.process_video(video_path)
    
    return {
        "total_frames": result["total_frames"],
        "frames_with_fire": result["frames_with_fire"],
        "fire_detected": result["fire_detected"],
        "overall_confidence": result["overall_confidence"],
        "frame_results": result["frame_results"][:10],  # Limit to first 10 frames for API response
        "metadata": {
            "model_version": "v1.0.0",
            "image_size": result["video_resolution"],
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "processing_time": "0.0s"  # Will be updated in main()
        }
    }

if __name__ == "__main__":
    main()
