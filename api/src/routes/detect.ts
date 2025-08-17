import { Router, Request, Response, NextFunction } from 'express';
import multer from 'multer';
import path from 'path';
import { v4 as uuidv4 } from 'uuid';
import { DetectionService } from '../services/DetectionService';
import { ValidationError } from '../types/errors';
import type { ApiResponse, DetectionResult, VideoDetectionResult } from '../types/detection';

const router = Router();

// Configure multer for file uploads
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, path.join(__dirname, '../../uploads/'));
  },
  filename: (req, file, cb) => {
    const uniqueName = `${uuidv4()}-${Date.now()}${path.extname(file.originalname)}`;
    cb(null, uniqueName);
  }
});

const fileFilter = (req: any, file: Express.Multer.File, cb: any) => {
  // Accept images and videos
  if (file.mimetype.startsWith('image/') || file.mimetype.startsWith('video/')) {
    cb(null, true);
  } else {
    cb(new ValidationError('Only image and video files are allowed'), false);
  }
};

const upload = multer({
  storage,
  fileFilter,
  limits: {
    fileSize: 50 * 1024 * 1024, // 50MB limit
  }
});

const detectionService = new DetectionService();

// POST /api/detect/image - Detect fire in a single image
router.post('/image', upload.single('image'), async (req: Request, res: Response<ApiResponse<DetectionResult>>, next: NextFunction) => {
  try {
    if (!req.file) {
      throw new ValidationError('No image file provided');
    }

    console.log(`🔍 Processing image: ${req.file.filename}`);

    const result = await detectionService.detectInImage(req.file.path, req.file.originalname);

    res.json({
      success: true,
      data: result,
      message: `Fire detection completed. Fire detected: ${result.fire_detected}`
    });

  } catch (error) {
    next(error);
  }
});

// POST /api/detect/video - Detect fire in video frames
router.post('/video', upload.single('video'), async (req: Request, res: Response<ApiResponse<VideoDetectionResult>>, next: NextFunction) => {
  try {
    if (!req.file) {
      throw new ValidationError('No video file provided');
    }

    console.log(`🎥 Processing video: ${req.file.filename}`);

    const result = await detectionService.detectInVideo(req.file.path, req.file.originalname);

    res.json({
      success: true,
      data: result,
      message: `Video analysis completed. Fire detected in ${result.frames_with_fire}/${result.total_frames} frames`
    });

  } catch (error) {
    next(error);
  }
});

// GET /api/detect/status - Get detection service status
router.get('/status', async (req: Request, res: Response, next: NextFunction) => {
  try {
    const status = await detectionService.getStatus();
    
    res.json({
      success: true,
      data: status,
      message: 'Detection service status'
    });
  } catch (error) {
    next(error);
  }
});

// GET /api/detect/history - Get recent detections
router.get('/history', async (req: Request, res: Response, next: NextFunction) => {
  try {
    const limit = parseInt(req.query.limit as string) || 10;
    const history = await detectionService.getDetectionHistory(limit);
    
    res.json({
      success: true,
      data: history,
      message: `Retrieved ${history.length} recent detections`
    });
  } catch (error) {
    next(error);
  }
});

// GET /api/detect/stats - Get detection statistics
router.get('/stats', async (req: Request, res: Response, next: NextFunction) => {
  try {
    const days = parseInt(req.query.days as string) || 7;
    const stats = await detectionService.getDetectionStats(days);
    
    res.json({
      success: true,
      data: stats,
      message: `Detection statistics for the last ${days} days`
    });
  } catch (error) {
    next(error);
  }
});

export { router as detectRoutes };
