import { spawn } from 'child_process';
import path from 'path';
import fs from 'fs';
import { DetectionResult, VideoDetectionResult, BoundingBox, DetectionMetadata } from '../types/detection';
import { ProcessingError } from '../types/errors';
import { DatabaseService } from './DatabaseService';

export class DetectionService {
  private pythonScriptPath: string;
  private modelPath: string;
  private dbService: DatabaseService;

  constructor() {
    // Path to Python script that will handle AI detection
    this.pythonScriptPath = path.join(__dirname, '../../../ai-core/detect.py');
    this.modelPath = path.join(__dirname, '../../../models/fire_detection_model.pth');
    this.dbService = new DatabaseService();
  }

  async detectInImage(imagePath: string, originalFilename?: string): Promise<DetectionResult> {
    const startTime = Date.now();
    
    try {
      // For now, let's create a mock response until we have the Python script ready
      if (!fs.existsSync(this.pythonScriptPath)) {
        console.log('⚠️  Python detection script not found, using mock response');
        const result = this.createMockDetectionResult(imagePath, startTime);
        
        // Save to database if available
        await this.saveDetectionToDb(imagePath, 'image', originalFilename || 'unknown', result, Date.now() - startTime);
        
        return result;
      }

      // Execute Python detection script
      const result = await this.executePythonDetection('image', imagePath);
      
      // Save to database
      await this.saveDetectionToDb(imagePath, 'image', originalFilename || 'unknown', result, Date.now() - startTime);
      
      return result;

    } catch (error) {
      console.error('❌ Error in image detection:', error);
      throw new ProcessingError(`Failed to process image: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
  }

  async detectInVideo(videoPath: string, originalFilename?: string): Promise<VideoDetectionResult> {
    const startTime = Date.now();
    
    try {
      // For now, let's create a mock response until we have the Python script ready
      if (!fs.existsSync(this.pythonScriptPath)) {
        console.log('⚠️  Python detection script not found, using mock response');
        const result = this.createMockVideoDetectionResult(videoPath, startTime);
        
        // Save to database if available
        await this.saveDetectionToDb(videoPath, 'video', originalFilename || 'unknown', result, Date.now() - startTime);
        
        return result;
      }

      // Execute Python detection script for video
      const result = await this.executePythonVideoDetection(videoPath);
      
      // Save to database
      await this.saveDetectionToDb(videoPath, 'video', originalFilename || 'unknown', result, Date.now() - startTime);
      
      return result;

    } catch (error) {
      console.error('❌ Error in video detection:', error);
      throw new ProcessingError(`Failed to process video: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
  }

  async getStatus(): Promise<any> {
    return {
      service: 'detection',
      status: 'ready',
      model_loaded: fs.existsSync(this.modelPath),
      python_script_available: fs.existsSync(this.pythonScriptPath),
      supported_formats: {
        images: ['jpg', 'jpeg', 'png', 'bmp'],
        videos: ['mp4', 'avi', 'mov', 'mkv']
      },
      version: '1.0.0'
    };
  }

  private async executePythonDetection(type: 'image' | 'video', filePath: string): Promise<DetectionResult> {
    return new Promise((resolve, reject) => {
      const pythonProcess = spawn('python', [this.pythonScriptPath, type, filePath]);
      
      let output = '';
      let errorOutput = '';

      pythonProcess.stdout.on('data', (data) => {
        output += data.toString();
      });

      pythonProcess.stderr.on('data', (data) => {
        errorOutput += data.toString();
      });

      pythonProcess.on('close', (code) => {
        if (code !== 0) {
          reject(new Error(`Python process exited with code ${code}: ${errorOutput}`));
          return;
        }

        try {
          const result = JSON.parse(output);
          resolve(result);
        } catch (error) {
          reject(new Error(`Failed to parse Python output: ${error}`));
        }
      });

      pythonProcess.on('error', (error) => {
        reject(new Error(`Failed to start Python process: ${error.message}`));
      });
    });
  }

  private async executePythonVideoDetection(videoPath: string): Promise<VideoDetectionResult> {
    // This will be similar to image detection but for video
    // For now, delegate to the same function and cast the result
    const result = await this.executePythonDetection('video', videoPath);
    return result as any; // TODO: Proper typing when Python script is ready
  }

  // Mock functions for development/testing
  private createMockDetectionResult(imagePath: string, startTime: number): DetectionResult {
    const processingTime = ((Date.now() - startTime) / 1000).toFixed(1);
    
    // Simulate random detection for demo purposes
    const fireDetected = Math.random() > 0.6; // 40% chance of fire detection
    const confidence = fireDetected ? 0.7 + Math.random() * 0.25 : Math.random() * 0.4;
    
    const boundingBoxes: BoundingBox[] = fireDetected ? [
      {
        x: Math.floor(Math.random() * 500),
        y: Math.floor(Math.random() * 300),
        width: 80 + Math.floor(Math.random() * 120),
        height: 60 + Math.floor(Math.random() * 100),
        confidence: confidence,
        class: Math.random() > 0.5 ? 'fire' : 'smoke'
      }
    ] : [];

    return {
      fire_detected: fireDetected,
      confidence: Number(confidence.toFixed(2)),
      bounding_boxes: boundingBoxes,
      metadata: {
        processing_time: `${processingTime}s`,
        model_version: 'mock-v1.0.0',
        image_size: '1920x1080', // Mock size
        timestamp: new Date().toISOString()
      }
    };
  }

  private createMockVideoDetectionResult(videoPath: string, startTime: number): VideoDetectionResult {
    const processingTime = ((Date.now() - startTime) / 1000).toFixed(1);
    const totalFrames = 30 + Math.floor(Math.random() * 120); // 30-150 frames
    const framesWithFire = Math.floor(totalFrames * Math.random() * 0.3); // Up to 30% of frames
    
    const frameResults = Array.from({ length: Math.min(10, totalFrames) }, (_, i) => ({
      frame_number: i + 1,
      timestamp: i * 0.033, // ~30fps
      fire_detected: Math.random() > 0.7,
      confidence: 0.6 + Math.random() * 0.3,
      bounding_boxes: []
    }));

    return {
      total_frames: totalFrames,
      frames_with_fire: framesWithFire,
      fire_detected: framesWithFire > 0,
      overall_confidence: framesWithFire > 0 ? 0.7 + Math.random() * 0.25 : Math.random() * 0.4,
      frame_results: frameResults,
      metadata: {
        processing_time: `${processingTime}s`,
        model_version: 'mock-v1.0.0',
        image_size: '1920x1080',
        timestamp: new Date().toISOString()
      }
    };
  }

  private async saveDetectionToDb(
    filePath: string, 
    fileType: 'image' | 'video', 
    originalFilename: string, 
    result: DetectionResult | VideoDetectionResult, 
    processingTime: number
  ): Promise<void> {
    try {
      const detectionId = await this.dbService.saveDetection(
        filePath, 
        fileType, 
        originalFilename, 
        result, 
        processingTime
      );
      console.log(`💾 Detection saved to database with ID: ${detectionId}`);
    } catch (error) {
      console.warn('⚠️  Failed to save to database, continuing without persistence:', error);
      // Don't throw error - detection should work even if DB is unavailable
    }
  }

  async getDetectionHistory(limit: number = 10) {
    try {
      return await this.dbService.getRecentDetections(limit);
    } catch (error) {
      console.warn('⚠️  Failed to get detection history from database:', error);
      return [];
    }
  }

  async getDetectionStats(days: number = 7) {
    try {
      return await this.dbService.getDetectionStats(days);
    } catch (error) {
      console.warn('⚠️  Failed to get detection stats from database:', error);
      return {
        total_detections: 0,
        fire_detections: 0,
        image_detections: 0,
        video_detections: 0,
        avg_fire_confidence: 0,
        avg_processing_time: 0,
        period_days: days
      };
    }
  }
}
