import { Pool, PoolClient } from 'pg';
import { DetectionResult, VideoDetectionResult } from '../types/detection';

export interface DetectionRecord {
  id: string;
  file_path: string;
  file_type: 'image' | 'video';
  original_filename: string;
  fire_detected: boolean;
  confidence: number;
  bounding_boxes: any[];
  metadata: any;
  created_at: Date;
  processing_time_ms: number;
  model_version: string;
}

export class DatabaseService {
  private pool: Pool;

  constructor() {
    // Debug das variáveis de ambiente
    console.log('🔍 Database config:', {
      user: process.env.DB_USER || 'postgres',
      host: process.env.DB_HOST || 'localhost', 
      database: process.env.DB_NAME || 'queimadai',
      password: process.env.DB_PASSWORD ? '***' : undefined,
      port: parseInt(process.env.DB_PORT || '5432'),
    });

    this.pool = new Pool({
      user: process.env.DB_USER || 'postgres',
      host: process.env.DB_HOST || 'localhost',
      database: process.env.DB_NAME || 'queimadai',
      password: process.env.DB_PASSWORD || 'postgres',
      port: parseInt(process.env.DB_PORT || '5432'),
      // Connection pool settings
      max: 20, // Maximum number of clients
      idleTimeoutMillis: 30000, // Close idle clients after 30 seconds
      connectionTimeoutMillis: 2000, // Return an error after 2 seconds if connection could not be established
    });

    // Test connection on startup
    this.testConnection();
  }

  async testConnection(): Promise<boolean> {
    try {
      const client = await this.pool.connect();
      await client.query('SELECT NOW()');
      client.release();
      console.log('✅ Database connection established');
      return true;
    } catch (error) {
      console.error('❌ Database connection failed:', error);
      console.log('⚠️  Continuing without database (using mock mode)');
      return false;
    }
  }

  async initializeDatabase(): Promise<void> {
    const client = await this.pool.connect();
    
    try {
      // Create detections table
      await client.query(`
        CREATE TABLE IF NOT EXISTS detections (
          id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
          file_path VARCHAR(500) NOT NULL,
          file_type VARCHAR(10) NOT NULL,
          original_filename VARCHAR(255) NOT NULL,
          fire_detected BOOLEAN NOT NULL,
          confidence DECIMAL(5,3) NOT NULL,
          bounding_boxes JSONB,
          metadata JSONB,
          created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
          processing_time_ms INTEGER,
          model_version VARCHAR(50)
        );
      `);

      // Create indexes
      await client.query(`
        CREATE INDEX IF NOT EXISTS idx_detections_created_at ON detections(created_at);
        CREATE INDEX IF NOT EXISTS idx_detections_fire_detected ON detections(fire_detected);
        CREATE INDEX IF NOT EXISTS idx_detections_file_type ON detections(file_type);
      `);

      console.log('✅ Database tables initialized');
    } catch (error) {
      console.error('❌ Failed to initialize database:', error);
      throw error;
    } finally {
      client.release();
    }
  }

  async saveDetection(
    filePath: string,
    fileType: 'image' | 'video',
    originalFilename: string,
    result: DetectionResult | VideoDetectionResult,
    processingTimeMs: number
  ): Promise<string> {
    const client = await this.pool.connect();
    
    try {
      const query = `
        INSERT INTO detections (
          file_path, file_type, original_filename, fire_detected, 
          confidence, bounding_boxes, metadata, processing_time_ms, model_version
        ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
        RETURNING id;
      `;

      const values = [
        filePath,
        fileType,
        originalFilename,
        result.fire_detected,
        'confidence' in result ? result.confidence : (result as VideoDetectionResult).overall_confidence,
        JSON.stringify('bounding_boxes' in result ? result.bounding_boxes : []),
        JSON.stringify(result.metadata),
        processingTimeMs,
        result.metadata.model_version
      ];

      const queryResult = await client.query(query, values);
      const detectionId = queryResult.rows[0].id;
      
      console.log(`💾 Detection saved to database: ${detectionId}`);
      return detectionId;
    } catch (error) {
      console.error('❌ Failed to save detection:', error);
      throw error;
    } finally {
      client.release();
    }
  }

  async getDetectionById(id: string): Promise<DetectionRecord | null> {
    const client = await this.pool.connect();
    
    try {
      const query = 'SELECT * FROM detections WHERE id = $1';
      const result = await client.query(query, [id]);
      
      if (result.rows.length === 0) {
        return null;
      }

      return result.rows[0] as DetectionRecord;
    } catch (error) {
      console.error('❌ Failed to get detection:', error);
      throw error;
    } finally {
      client.release();
    }
  }

  async getRecentDetections(limit: number = 10): Promise<DetectionRecord[]> {
    const client = await this.pool.connect();
    
    try {
      const query = `
        SELECT * FROM detections 
        ORDER BY created_at DESC 
        LIMIT $1
      `;
      const result = await client.query(query, [limit]);
      
      return result.rows as DetectionRecord[];
    } catch (error) {
      console.error('❌ Failed to get recent detections:', error);
      throw error;
    } finally {
      client.release();
    }
  }

  async getDetectionStats(days: number = 7): Promise<any> {
    const client = await this.pool.connect();
    
    try {
      const query = `
        SELECT 
          COUNT(*) as total_detections,
          COUNT(*) FILTER (WHERE fire_detected = true) as fire_detections,
          COUNT(*) FILTER (WHERE file_type = 'image') as image_detections,
          COUNT(*) FILTER (WHERE file_type = 'video') as video_detections,
          AVG(confidence) FILTER (WHERE fire_detected = true) as avg_fire_confidence,
          AVG(processing_time_ms) as avg_processing_time
        FROM detections 
        WHERE created_at >= NOW() - INTERVAL '${days} days'
      `;
      
      const result = await client.query(query);
      const stats = result.rows[0];
      
      // Convert string numbers to proper types
      return {
        total_detections: parseInt(stats.total_detections),
        fire_detections: parseInt(stats.fire_detections),
        image_detections: parseInt(stats.image_detections),
        video_detections: parseInt(stats.video_detections),
        avg_fire_confidence: parseFloat(stats.avg_fire_confidence) || 0,
        avg_processing_time: parseFloat(stats.avg_processing_time) || 0,
        period_days: days
      };
    } catch (error) {
      console.error('❌ Failed to get detection stats:', error);
      throw error;
    } finally {
      client.release();
    }
  }

  async close(): Promise<void> {
    await this.pool.end();
    console.log('🔌 Database connection pool closed');
  }
}
