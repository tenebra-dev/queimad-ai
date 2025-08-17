"""
Video Processor Class
Handles video file processing for fire detection
"""

import cv2
import numpy as np
from typing import List, Dict, Any

class VideoProcessor:
    def __init__(self, fire_detector):
        self.fire_detector = fire_detector
        self.frame_skip = 5  # Process every 5th frame for efficiency
        
    def process_video(self, video_path: str) -> Dict[str, Any]:
        """
        Process a video file and detect fire in frames
        Args:
            video_path: Path to video file
        Returns:
            Dictionary with video analysis results
        """
        try:
            # Open video file
            cap = cv2.VideoCapture(video_path)
            
            if not cap.isOpened():
                raise ValueError(f"Could not open video file: {video_path}")
            
            # Get video properties
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            fps = cap.get(cv2.CAP_PROP_FPS)
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            
            frame_results = []
            frames_with_fire = 0
            frame_number = 0
            processed_frames = 0
            
            print(f"📹 Processing video: {total_frames} frames, {fps:.1f} FPS, {width}x{height}")
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                frame_number += 1
                
                # Skip frames for efficiency
                if frame_number % self.frame_skip != 0:
                    continue
                
                processed_frames += 1
                
                # Convert BGR to RGB
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Detect fire in current frame
                detection_result = self.fire_detector.detect(frame_rgb)
                
                # Calculate timestamp
                timestamp = frame_number / fps if fps > 0 else 0
                
                frame_result = {
                    "frame_number": frame_number,
                    "timestamp": round(timestamp, 2),
                    "fire_detected": detection_result["fire_detected"],
                    "confidence": detection_result["confidence"],
                    "bounding_boxes": detection_result["bounding_boxes"]
                }
                
                frame_results.append(frame_result)
                
                if detection_result["fire_detected"]:
                    frames_with_fire += 1
                
                # Print progress
                if processed_frames % 10 == 0:
                    progress = (frame_number / total_frames) * 100
                    print(f"Progress: {progress:.1f}% - Fire detected in {frames_with_fire} frames so far")
            
            cap.release()
            
            # Calculate overall statistics
            fire_detected = frames_with_fire > 0
            
            # Calculate overall confidence as average of fire detections
            fire_confidences = [fr["confidence"] for fr in frame_results if fr["fire_detected"]]
            overall_confidence = np.mean(fire_confidences) if fire_confidences else 0.0
            
            result = {
                "total_frames": total_frames,
                "processed_frames": processed_frames,
                "frames_with_fire": frames_with_fire,
                "fire_detected": fire_detected,
                "overall_confidence": round(overall_confidence, 3),
                "frame_results": frame_results,
                "video_resolution": f"{width}x{height}",
                "fps": fps,
                "duration_seconds": total_frames / fps if fps > 0 else 0
            }
            
            print(f"✅ Video processing complete: {frames_with_fire}/{processed_frames} frames with fire")
            
            return result
            
        except Exception as e:
            print(f"❌ Video processing failed: {e}")
            raise
    
    def extract_frames_with_fire(self, video_path: str, output_dir: str) -> List[str]:
        """
        Extract frames that contain fire to separate image files
        Args:
            video_path: Path to video file
            output_dir: Directory to save extracted frames
        Returns:
            List of saved frame file paths
        """
        import os
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        result = self.process_video(video_path)
        
        # Re-open video to extract specific frames
        cap = cv2.VideoCapture(video_path)
        saved_frames = []
        
        for frame_result in result["frame_results"]:
            if frame_result["fire_detected"]:
                frame_number = frame_result["frame_number"]
                
                # Seek to specific frame
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number - 1)
                ret, frame = cap.read()
                
                if ret:
                    # Save frame
                    filename = f"fire_frame_{frame_number:06d}.jpg"
                    filepath = os.path.join(output_dir, filename)
                    cv2.imwrite(filepath, frame)
                    saved_frames.append(filepath)
        
        cap.release()
        
        print(f"💾 Extracted {len(saved_frames)} frames with fire to {output_dir}")
        
        return saved_frames
