"""
Visual Interface for Fire Detection
Shows video playback with real-time fire detection overlays
"""

import cv2
import numpy as np
import sys
import os
from pathlib import Path

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from fire_detector import FireDetector

class FireDetectionUI:
    def __init__(self, model_path=None):
        self.detector = FireDetector(model_path)
        self.colors = {
            'fire': (0, 0, 255),      # Red for fire
            'smoke': (255, 165, 0),   # Orange for smoke
            'text': (255, 255, 255),  # White for text
            'background': (0, 0, 0)   # Black background for text
        }
        
    def process_video_realtime(self, video_path, output_path=None, show_live=True):
        """
        Process video with real-time fire detection visualization
        Args:
            video_path: Path to input video
            output_path: Path to save output video (optional)
            show_live: Whether to show live preview window
        """
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            print(f"❌ Error: Could not open video {video_path}")
            return
        
        # Get video properties
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        print(f"📹 Processing video: {width}x{height}, {fps} FPS, {total_frames} frames")
        
        # Setup output video writer if saving
        out = None
        if output_path:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        frame_count = 0
        fire_detections = 0
        
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                frame_count += 1
                
                # Convert BGR to RGB for detection
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Detect fire
                detection_result = self.detector.detect(frame_rgb)
                
                # Draw overlays on frame
                annotated_frame = self.draw_detection_overlay(
                    frame, detection_result, frame_count, total_frames
                )
                
                if detection_result['fire_detected']:
                    fire_detections += 1
                
                # Save frame if output is specified
                if out:
                    out.write(annotated_frame)
                
                # Show live preview
                if show_live:
                    cv2.imshow('🔥 QueimadAI - Fire Detection', annotated_frame)
                    
                    # Controls: 'q' to quit, 'p' to pause
                    key = cv2.waitKey(1) & 0xFF
                    if key == ord('q'):
                        print("\n⏹️  Stopping video processing...")
                        break
                    elif key == ord('p'):
                        print("⏸️  Paused. Press any key to continue...")
                        cv2.waitKey(0)
                
                # Print progress
                if frame_count % (fps * 2) == 0:  # Every 2 seconds
                    progress = (frame_count / total_frames) * 100
                    print(f"Progress: {progress:.1f}% - Fire detected in {fire_detections} frames")
        
        finally:
            # Cleanup
            cap.release()
            if out:
                out.release()
            if show_live:
                cv2.destroyAllWindows()
            
            print(f"\n✅ Processing complete!")
            print(f"📊 Stats: {fire_detections}/{frame_count} frames with fire ({fire_detections/frame_count*100:.1f}%)")
            if output_path:
                print(f"💾 Output saved to: {output_path}")
    
    def draw_detection_overlay(self, frame, detection_result, frame_num, total_frames):
        """
        Draw detection overlays on frame
        """
        # Make a copy to avoid modifying original
        overlay_frame = frame.copy()
        
        # Draw bounding boxes
        for bbox in detection_result['bounding_boxes']:
            x, y, w, h = bbox['x'], bbox['y'], bbox['width'], bbox['height']
            confidence = bbox['confidence']
            class_name = bbox['class']
            
            # Choose color based on class
            color = self.colors.get(class_name, self.colors['fire'])
            
            # Draw bounding box
            cv2.rectangle(overlay_frame, (x, y), (x + w, y + h), color, 2)
            
            # Draw label with confidence
            label = f"{class_name.upper()}: {confidence:.2f}"
            label_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
            
            # Draw label background
            cv2.rectangle(overlay_frame, 
                         (x, y - label_size[1] - 10), 
                         (x + label_size[0], y), 
                         color, -1)
            
            # Draw label text
            cv2.putText(overlay_frame, label, (x, y - 5), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, self.colors['text'], 2)
        
        # Draw status overlay
        self.draw_status_overlay(overlay_frame, detection_result, frame_num, total_frames)
        
        return overlay_frame
    
    def draw_status_overlay(self, frame, detection_result, frame_num, total_frames):
        """
        Draw status information overlay
        """
        h, w = frame.shape[:2]
        
        # Status background
        overlay_height = 120
        cv2.rectangle(frame, (0, 0), (w, overlay_height), (0, 0, 0), -1)
        cv2.rectangle(frame, (0, 0), (w, overlay_height), (100, 100, 100), 2)
        
        # Main status
        fire_status = "🔥 FIRE DETECTED" if detection_result['fire_detected'] else "✅ NO FIRE"
        status_color = (0, 0, 255) if detection_result['fire_detected'] else (0, 255, 0)
        
        cv2.putText(frame, fire_status, (20, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, status_color, 2)
        
        # Confidence
        confidence_text = f"Confidence: {detection_result['confidence']:.3f}"
        cv2.putText(frame, confidence_text, (20, 55), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.colors['text'], 1)
        
        # Frame info
        frame_text = f"Frame: {frame_num}/{total_frames}"
        cv2.putText(frame, frame_text, (20, 75), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.colors['text'], 1)
        
        # Detection count
        detection_count = len(detection_result['bounding_boxes'])
        count_text = f"Detections: {detection_count}"
        cv2.putText(frame, count_text, (20, 95), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.colors['text'], 1)
        
        # Controls
        controls_text = "Controls: 'Q' to quit, 'P' to pause"
        cv2.putText(frame, controls_text, (w - 300, h - 20), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, self.colors['text'], 1)

def main():
    if len(sys.argv) < 2:
        print("Usage: python video_ui.py <video_path> [output_path]")
        print("Example: python video_ui.py test_video.mp4 output_with_detection.mp4")
        sys.exit(1)
    
    video_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not os.path.exists(video_path):
        print(f"❌ Error: Video file not found: {video_path}")
        sys.exit(1)
    
    # Initialize UI
    ui = FireDetectionUI()
    
    print("🔥 QueimadAI - Video Fire Detection UI")
    print("=====================================")
    print(f"📹 Input video: {video_path}")
    if output_path:
        print(f"💾 Output video: {output_path}")
    print("\nStarting video processing...")
    print("Controls: 'Q' to quit, 'P' to pause\n")
    
    # Process video
    ui.process_video_realtime(video_path, output_path, show_live=True)

if __name__ == "__main__":
    main()
