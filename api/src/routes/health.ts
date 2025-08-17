import { Router, Request, Response } from 'express';

const router = Router();

router.get('/', (req: Request, res: Response) => {
  res.json({
    success: true,
    message: 'QueimadAI API is healthy! 🔥',
    timestamp: new Date().toISOString(),
    version: '1.0.0',
    endpoints: {
      'POST /api/detect/image': 'Detect fire in a single image',
      'POST /api/detect/video': 'Detect fire in video frames',
      'GET /api/health': 'Health check'
    },
    system: {
      uptime: process.uptime(),
      memory: process.memoryUsage(),
      platform: process.platform,
      node_version: process.version
    }
  });
});

router.get('/ai', (req: Request, res: Response) => {
  // TODO: Add AI service health check
  res.json({
    success: true,
    message: 'AI service health check',
    ai_service: {
      status: 'checking...',
      model_loaded: false,
      last_prediction: null
    }
  });
});

export { router as healthRoutes };
