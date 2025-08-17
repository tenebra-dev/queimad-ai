import { Request, Response, NextFunction } from 'express';
import { ApiError } from '../types/errors';
import logger from '../utils/logger';

export const errorHandler = (
  err: Error | ApiError,
  req: Request,
  res: Response,
  next: NextFunction
): void => {
  const requestId = (req as any).requestId || 'unknown';
  let statusCode = 500;
  let message = 'Internal Server Error';

  // If it's an operational error (our custom errors)
  if ('statusCode' in err && 'isOperational' in err) {
    statusCode = err.statusCode;
    message = err.message;
  } else if (err.name === 'ValidationError') {
    statusCode = 400;
    message = err.message;
  } else if (err.name === 'CastError') {
    statusCode = 400;
    message = 'Invalid data format';
  } else if (err.name === 'MulterError') {
    statusCode = 400;
    message = `File upload error: ${err.message}`;
  }

  // Log estruturado do erro
  logger.error({
    message: 'Request error',
    error: message,
    errorName: err.name,
    statusCode,
    requestId,
    method: req.method,
    url: req.url,
    stack: err.stack,
    action: 'error.handled'
  });

  res.status(statusCode).json({
    success: false,
    error: message,
    requestId,
    ...(process.env.NODE_ENV === 'development' && {
      stack: err.stack,
      details: err
    })
  });
};
