export interface ApiError extends Error {
  statusCode: number;
  isOperational: boolean;
}

export class AppError extends Error implements ApiError {
  public readonly statusCode: number;
  public readonly isOperational: boolean = true;

  constructor(message: string, statusCode: number = 500) {
    super(message);
    this.statusCode = statusCode;

    Error.captureStackTrace(this, this.constructor);
  }
}

export class ValidationError extends AppError {
  constructor(message: string) {
    super(message, 400);
  }
}

export class NotFoundError extends AppError {
  constructor(message: string = 'Resource not found') {
    super(message, 404);
  }
}

export class ProcessingError extends AppError {
  constructor(message: string) {
    super(message, 422);
  }
}
