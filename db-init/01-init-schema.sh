#!/bin/bash
set -e

# Script que roda automaticamente quando o container PostgreSQL inicia
echo "🗄️  Initializing QueimadAI Database Schema..."

# Criar tabelas
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    -- Enable UUID extension
    CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
    
    -- Create detections table
    CREATE TABLE IF NOT EXISTS detections (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        file_path VARCHAR(500) NOT NULL,
        file_type VARCHAR(10) NOT NULL CHECK (file_type IN ('image', 'video')),
        original_filename VARCHAR(255) NOT NULL,
        fire_detected BOOLEAN NOT NULL,
        confidence DECIMAL(5,3) NOT NULL CHECK (confidence >= 0 AND confidence <= 1),
        bounding_boxes JSONB DEFAULT '[]'::jsonb,
        metadata JSONB DEFAULT '{}'::jsonb,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        processing_time_ms INTEGER CHECK (processing_time_ms >= 0),
        model_version VARCHAR(50)
    );

    -- Create indexes for performance
    CREATE INDEX IF NOT EXISTS idx_detections_created_at ON detections(created_at DESC);
    CREATE INDEX IF NOT EXISTS idx_detections_fire_detected ON detections(fire_detected);
    CREATE INDEX IF NOT EXISTS idx_detections_file_type ON detections(file_type);
    CREATE INDEX IF NOT EXISTS idx_detections_confidence ON detections(confidence DESC);
    CREATE INDEX IF NOT EXISTS idx_detections_model_version ON detections(model_version);

    -- Create cameras table for future use
    CREATE TABLE IF NOT EXISTS cameras (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        name VARCHAR(100) NOT NULL,
        location VARCHAR(200),
        latitude DECIMAL(10, 8),
        longitude DECIMAL(11, 8),
        status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'inactive', 'maintenance')),
        api_key VARCHAR(255) UNIQUE,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );

    -- Create detection_stats table for analytics
    CREATE TABLE IF NOT EXISTS detection_stats (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        camera_id UUID REFERENCES cameras(id) ON DELETE SET NULL,
        date DATE NOT NULL,
        total_detections INTEGER DEFAULT 0 CHECK (total_detections >= 0),
        fire_detections INTEGER DEFAULT 0 CHECK (fire_detections >= 0),
        avg_confidence DECIMAL(5,3) CHECK (avg_confidence >= 0 AND avg_confidence <= 1),
        max_confidence DECIMAL(5,3) CHECK (max_confidence >= 0 AND max_confidence <= 1),
        avg_processing_time DECIMAL(10,2),
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        UNIQUE(camera_id, date)
    );

    -- Create indexes for stats
    CREATE INDEX IF NOT EXISTS idx_detection_stats_date ON detection_stats(date DESC);
    CREATE INDEX IF NOT EXISTS idx_detection_stats_camera_date ON detection_stats(camera_id, date);

    -- Insert sample data for testing
    INSERT INTO detections (
        file_path, file_type, original_filename, fire_detected, 
        confidence, bounding_boxes, metadata, processing_time_ms, model_version
    ) VALUES 
    (
        '/uploads/sample1.jpg', 'image', 'forest_fire_sample.jpg', true, 
        0.895, 
        '[{"x": 120, "y": 80, "width": 150, "height": 100, "confidence": 0.895, "class": "fire"}]'::jsonb,
        '{"processing_time": "1.2s", "image_size": "1920x1080", "timestamp": "2025-08-17T10:00:00Z"}'::jsonb,
        1200, 'mock-v1.0.0'
    ),
    (
        '/uploads/sample2.jpg', 'image', 'no_fire_sample.jpg', false, 
        0.125, 
        '[]'::jsonb,
        '{"processing_time": "0.8s", "image_size": "1280x720", "timestamp": "2025-08-17T10:05:00Z"}'::jsonb,
        800, 'mock-v1.0.0'
    ),
    (
        '/uploads/sample_video.mp4', 'video', 'forest_surveillance.mp4', true, 
        0.756, 
        '[]'::jsonb,
        '{"processing_time": "15.3s", "total_frames": 450, "frames_with_fire": 23, "video_resolution": "1920x1080"}'::jsonb,
        15300, 'mock-v1.0.0'
    ) ON CONFLICT DO NOTHING;

    -- Insert sample camera
    INSERT INTO cameras (name, location, latitude, longitude, status) VALUES 
    ('Camera Principal', 'Floresta Nacional de Brasília', -15.7801, -47.9292, 'active'),
    ('Camera Backup', 'Parque Nacional da Chapada dos Veadeiros', -14.1111, -47.6167, 'active')
    ON CONFLICT DO NOTHING;

EOSQL

echo "✅ Database schema initialized successfully!"
echo "📊 Sample data inserted for testing"
