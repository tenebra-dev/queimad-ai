import winston from 'winston';
import path from 'path';

// Definir níveis de log customizados
const levels = {
  error: 0,
  warn: 1,
  info: 2,
  http: 3,
  debug: 4,
};

// Definir cores para cada nível
const colors = {
  error: 'red',
  warn: 'yellow',
  info: 'green',
  http: 'magenta',
  debug: 'white',
};

winston.addColors(colors);

// Formato para desenvolvimento (console)
const devFormat = winston.format.combine(
  winston.format.timestamp({ format: 'YYYY-MM-DD HH:mm:ss:ms' }),
  winston.format.colorize({ all: true }),
  winston.format.printf(
    (info) => `${info.timestamp} ${info.level}: ${info.message}`
  )
);

// Formato para produção (JSON estruturado)
const prodFormat = winston.format.combine(
  winston.format.timestamp(),
  winston.format.errors({ stack: true }),
  winston.format.json()
);

// Configurar transports
const transports = [];

// Console sempre ativo
transports.push(
  new winston.transports.Console({
    format: process.env.NODE_ENV === 'production' ? prodFormat : devFormat,
  })
);

// Arquivos apenas em produção
if (process.env.NODE_ENV === 'production') {
  transports.push(
    new winston.transports.File({
      filename: path.join(__dirname, '../../logs/error.log'),
      level: 'error',
      format: prodFormat,
    }),
    new winston.transports.File({
      filename: path.join(__dirname, '../../logs/combined.log'),
      format: prodFormat,
    })
  );
}

// Criar logger
const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || (process.env.NODE_ENV === 'production' ? 'info' : 'debug'),
  levels,
  format: prodFormat,
  transports,
  exitOnError: false,
});

// Logger específico para requests HTTP
export const httpLogger = winston.createLogger({
  level: 'http',
  levels,
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  transports: [
    new winston.transports.Console({
      format: devFormat,
    }),
  ],
});

// Função helper para logs estruturados
export const createLogMessage = (
  message: string,
  metadata?: Record<string, any>
) => {
  return {
    message,
    service: 'queimadai-api',
    environment: process.env.NODE_ENV || 'development',
    version: process.env.npm_package_version || '1.0.0',
    ...metadata,
  };
};

// Logs específicos do domínio
export const detectionLogger = {
  started: (requestId: string, fileType: string, fileName?: string) =>
    logger.info(createLogMessage('Detection started', {
      requestId,
      fileType,
      fileName,
      action: 'detection.started'
    })),

  completed: (requestId: string, result: any, processingTime: number) =>
    logger.info(createLogMessage('Detection completed', {
      requestId,
      result: {
        hasSmoke: result.hasSmoke,
        hasFire: result.hasFire,
        confidence: result.confidence
      },
      processingTime,
      action: 'detection.completed'
    })),

  failed: (requestId: string, error: string, processingTime?: number) =>
    logger.error(createLogMessage('Detection failed', {
      requestId,
      error,
      processingTime,
      action: 'detection.failed'
    })),
};

export const databaseLogger = {
  connected: (database: string) =>
    logger.info(createLogMessage('Database connected', {
      database,
      action: 'database.connected'
    })),

  connectionFailed: (database: string, error: string) =>
    logger.error(createLogMessage('Database connection failed', {
      database,
      error,
      action: 'database.connection_failed'
    })),

  queryExecuted: (query: string, duration: number) =>
    logger.debug(createLogMessage('Database query executed', {
      query: query.substring(0, 100) + (query.length > 100 ? '...' : ''),
      duration,
      action: 'database.query_executed'
    })),
};

export const serverLogger = {
  started: (port: number) =>
    logger.info(createLogMessage('Server started', {
      port,
      action: 'server.started'
    })),

  shutdown: (reason: string) =>
    logger.info(createLogMessage('Server shutting down', {
      reason,
      action: 'server.shutdown'
    })),
};

export default logger;
