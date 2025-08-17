#!/usr/bin/env node

/**
 * Script to initialize PostgreSQL database
 * Usage: node scripts/init-db.js
 */

require('dotenv').config();
const { Pool } = require('pg');

async function initDatabase() {
  console.log('🗄️  Initializing QueimadAI Database...');
  
  // Check if database config is provided
  if (!process.env.DB_HOST && !process.env.DB_USER) {
    console.log('⚠️  No database configuration found in .env file');
    console.log('💡 Database is optional for MVP - system will use mock data');
    console.log('📖 See DATABASE-STRATEGY.md for setup instructions');
    return;
  }

  const pool = new Pool({
    user: process.env.DB_USER || 'postgres',
    host: process.env.DB_HOST || 'localhost',
    database: 'postgres', // Connect to default database first
    password: process.env.DB_PASSWORD || 'postgres',
    port: parseInt(process.env.DB_PORT || '5432'),
  });

  try {
    // Test connection
    console.log('🔌 Testing database connection...');
    const client = await pool.connect();
    await client.query('SELECT NOW()');
    console.log('✅ Database connection successful');

    // Create database if it doesn't exist
    const dbName = process.env.DB_NAME || 'queimadai';
    console.log(`🏗️  Creating database '${dbName}' if it doesn't exist...`);
    
    try {
      await client.query(`CREATE DATABASE ${dbName}`);
      console.log(`✅ Database '${dbName}' created`);
    } catch (error) {
      if (error.code === '42P04') {
        console.log(`ℹ️  Database '${dbName}' already exists`);
      } else {
        throw error;
      }
    }
    
    client.release();

    // Connect to the actual database and create tables
    const appPool = new Pool({
      user: process.env.DB_USER || 'postgres',
      host: process.env.DB_HOST || 'localhost',
      database: dbName,
      password: process.env.DB_PASSWORD || 'postgres',
      port: parseInt(process.env.DB_PORT || '5432'),
    });

    const appClient = await appPool.connect();

    console.log('📋 Creating tables...');

    // Create detections table
    await appClient.query(`
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
    await appClient.query(`
      CREATE INDEX IF NOT EXISTS idx_detections_created_at ON detections(created_at);
      CREATE INDEX IF NOT EXISTS idx_detections_fire_detected ON detections(fire_detected);
      CREATE INDEX IF NOT EXISTS idx_detections_file_type ON detections(file_type);
    `);

    console.log('✅ Tables and indexes created successfully');

    // Insert sample data for testing
    console.log('📝 Inserting sample data...');
    await appClient.query(`
      INSERT INTO detections (
        file_path, file_type, original_filename, fire_detected, 
        confidence, bounding_boxes, metadata, processing_time_ms, model_version
      ) VALUES 
      (
        '/uploads/sample1.jpg', 'image', 'forest_fire_sample.jpg', true, 
        0.895, '[{"x": 120, "y": 80, "width": 150, "height": 100, "confidence": 0.895, "class": "fire"}]',
        '{"processing_time": "1.2s", "image_size": "1920x1080", "timestamp": "2025-08-17T10:00:00Z"}',
        1200, 'mock-v1.0.0'
      ),
      (
        '/uploads/sample2.jpg', 'image', 'no_fire_sample.jpg', false, 
        0.125, '[]',
        '{"processing_time": "0.8s", "image_size": "1280x720", "timestamp": "2025-08-17T10:05:00Z"}',
        800, 'mock-v1.0.0'
      )
    `);

    console.log('✅ Sample data inserted');

    appClient.release();
    await appPool.end();
    await pool.end();

    console.log('🎉 Database initialization complete!');
    console.log('🚀 You can now start the API with: pnpm dev');

  } catch (error) {
    console.error('❌ Database initialization failed:', error.message);
    console.log('\n💡 Troubleshooting:');
    console.log('1. Make sure PostgreSQL is running');
    console.log('2. Check your .env database credentials');
    console.log('3. Ensure the database user has CREATE DATABASE privileges');
    console.log('4. The system will work without database (using mock data)');
    process.exit(1);
  }
}

if (require.main === module) {
  initDatabase();
}

module.exports = initDatabase;
