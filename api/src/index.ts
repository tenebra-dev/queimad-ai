import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import dotenv from 'dotenv';
import path from 'path';

import { errorHandler } from './middleware/errorHandler';
import { detectRoutes } from './routes/detect';
import { healthRoutes } from './routes/health';
import logger, { serverLogger, httpLogger } from './utils/logger';

// Load environment variables
dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(helmet());
app.use(cors());

// Custom HTTP logging middleware
app.use((req, res, next) => {
  const start = Date.now();
  const requestId = Math.random().toString(36).substring(7);
  
  // Adicionar requestId ao request
  (req as any).requestId = requestId;
  
  res.on('finish', () => {
    const duration = Date.now() - start;
    httpLogger.http({
      message: 'HTTP Request',
      requestId,
      method: req.method,
      url: req.url,
      statusCode: res.statusCode,
      duration,
      userAgent: req.get('User-Agent'),
      ip: req.ip,
    });
  });
  
  next();
});

app.use(express.json({ limit: '50mb' }));
app.use(express.urlencoded({ extended: true, limit: '50mb' }));

// Create uploads directory if it doesn't exist
const uploadsDir = path.join(__dirname, '../uploads');
// Ensure uploads directory exists (will be handled by multer)

// Routes
app.use('/api/health', healthRoutes);
app.use('/api/detect', detectRoutes);

// Root endpoint
app.get('/', (req, res) => {
  res.json({
    message: '🔥 QueimadAI - Sistema de Detecção de Queimadas',
    version: '1.0.0',
    status: 'online',
    docs: '/api/health',
    endpoints: {
      health: '/api/health',
      detect_image: 'POST /api/detect/image',
      detect_video: 'POST /api/detect/video'
    }
  });
});

// Error handling middleware (must be last)
app.use(errorHandler);

// Start server
app.listen(PORT, () => {
  serverLogger.started(Number(PORT));
  logger.info(`📖 Health check: http://localhost:${PORT}/api/health`);
  logger.info(`🚀 Ready to detect fires!`);
});

export default app;
