export interface DetectionResult {
  fire_detected: boolean;
  confidence: number;
  bounding_boxes: BoundingBox[];
  metadata: DetectionMetadata;
}

export interface BoundingBox {
  x: number;
  y: number;
  width: number;
  height: number;
  confidence: number;
  class: 'fire' | 'smoke';
}

export interface DetectionMetadata {
  processing_time: string;
  model_version: string;
  image_size: string;
  timestamp: string;
}

export interface ApiResponse<T = any> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}

export interface VideoDetectionResult {
  total_frames: number;
  frames_with_fire: number;
  fire_detected: boolean;
  overall_confidence: number;
  frame_results: FrameDetection[];
  metadata: DetectionMetadata;
}

export interface FrameDetection {
  frame_number: number;
  timestamp: number;
  fire_detected: boolean;
  confidence: number;
  bounding_boxes: BoundingBox[];
}
