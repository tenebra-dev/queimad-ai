# 🗄️ Database Strategy - QueimadAI

## ✅ Status: **IMPLEMENTADO E FUNCIONANDO**

PostgreSQL + Redis rodando em Docker com schema criado e dados de exemplo.

## Recomendação: PostgreSQL + Redis

### Por que PostgreSQL como principal?

✅ **Você já tem experiência** - Maior produtividade
✅ **Estrutura de dados bem definida** - Detecções, usuários, câmeras
✅ **ACID compliance** - Importante para logs de detecção
✅ **JSON support** - Para metadata flexível
✅ **Spatial extensions** - PostGIS para coordenadas geográficas futuras
✅ **Performance excelente** - Para relatórios e analytics

### Por que Redis como complemento?

✅ **Cache de resultados** - Evitar reprocessamento
✅ **Queue de jobs** - Processamento assíncrono de vídeos
✅ **Rate limiting** - Controle de uso da API
✅ **Session storage** - Para futuro dashboard web
✅ **Real-time notifications** - WebSocket support

## 📊 Schema Principal (PostgreSQL)

```sql
-- Tabela de detecções
CREATE TABLE detections (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    file_path VARCHAR(500) NOT NULL,
    file_type VARCHAR(10) NOT NULL, -- 'image' ou 'video'
    original_filename VARCHAR(255) NOT NULL,
    fire_detected BOOLEAN NOT NULL,
    confidence DECIMAL(5,3) NOT NULL,
    bounding_boxes JSONB, -- Array de bounding boxes
    metadata JSONB, -- Processing time, model version, etc
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    processing_time_ms INTEGER,
    model_version VARCHAR(50)
);

-- Tabela de câmeras (futuro)
CREATE TABLE cameras (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    location VARCHAR(200),
    coordinates POINT, -- Para PostGIS
    status VARCHAR(20) DEFAULT 'active',
    api_key VARCHAR(255) UNIQUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabela de estatísticas por período
CREATE TABLE detection_stats (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    camera_id UUID REFERENCES cameras(id),
    date DATE NOT NULL,
    total_detections INTEGER DEFAULT 0,
    fire_detections INTEGER DEFAULT 0,
    avg_confidence DECIMAL(5,3),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índices para performance
CREATE INDEX idx_detections_created_at ON detections(created_at);
CREATE INDEX idx_detections_fire_detected ON detections(fire_detected);
CREATE INDEX idx_detections_file_type ON detections(file_type);
CREATE INDEX idx_detection_stats_date ON detection_stats(date);
```

## 🚀 Cache Strategy (Redis)

```javascript
// Estrutura de cache
{
  // Cache de resultados por hash do arquivo
  "detection:hash:abc123": {
    "result": {...},
    "expires": 3600 // 1 hora
  },
  
  // Queue de processamento
  "queue:video-processing": [...],
  
  // Rate limiting
  "rate:api:192.168.1.1": {
    "count": 10,
    "expires": 60 // Por minuto
  },
  
  // Stats em tempo real
  "stats:today": {
    "total_requests": 150,
    "fire_detections": 23,
    "avg_confidence": 0.87
  }
}
```

## 📈 Vantagens desta Abordagem

### Para MVP:
- **PostgreSQL**: Armazena histórico de detecções
- **Sem Redis inicialmente**: Simplifica setup

### Para Produção:
- **PostgreSQL**: Analytics, relatórios, histórico
- **Redis**: Performance, cache, real-time

## 🛠️ Implementação Gradual

### Fase 1 (MVP) - Só PostgreSQL
- Tabela `detections` básica
- Logs de todas as detecções
- Queries simples para stats

### Fase 2 - Adicionar Redis
- Cache de resultados
- Queue para vídeos pesados
- Rate limiting

### Fase 3 - Features Avançadas
- PostGIS para mapas
- Time-series para analytics
- WebSocket notifications

## 💡 Alternativas Consideradas

### MongoDB
❌ **Não recomendo** para este caso:
- Você não tem experiência
- Estrutura de dados é bem definida
- PostgreSQL JSON é suficiente
- Menor ecossistema para geolocalização

### InfluxDB (Time-series)
✅ **Consideraria** para Analytics futuro:
- Excelente para métricas temporais
- Mas adiciona complexidade
- PostgreSQL resolve bem inicialmente

### SQLite
✅ **OK para desenvolvimento**:
- Zero setup
- Mas limitado para produção
- Não escala para múltiplas câmeras

## 🎯 Decisão Final

**Start com PostgreSQL**, adicione Redis quando precisar de:
- Cache para melhor performance
- Queue para processamento pesado
- Rate limiting para API pública

Essa abordagem maximiza sua produtividade atual e permite escalabilidade futura sem over-engineering no MVP.
