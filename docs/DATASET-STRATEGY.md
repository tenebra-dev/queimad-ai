# 🔥 Dataset Strategy - Queimadas Brasileiras

## 🎯 Objetivo: 1000+ imagens anotadas de queimadas brasileiras

### 📊 Fontes de Dados Identificadas

#### 1. **INPE - Instituto Nacional de Pesquisas Espaciais**
- **Portal de Queimadas**: https://queimadas.dgi.inpe.br/queimadas/
- **Dados**: Focos de calor, coordenadas, timestamps
- **Formato**: CSV + API REST
- **Vantagem**: Dados oficiais brasileiros

#### 2. **Sentinel Hub / Copernicus**
- **Sentinel-2**: Imagens de satélite gratuitas
- **SWIR bands**: Ideal para detecção de fogo
- **Resolução**: 10-60m por pixel
- **Cobertura**: Brasil completo

#### 3. **NASA FIRMS**
- **MODIS/VIIRS**: Detecção de incêndios em tempo real
- **API**: https://firms.modaps.eosdis.nasa.gov/
- **Dados**: Brasil + coordenadas + confidence

#### 4. **Imagens Web + Validation**
- **Google Images**: Busca específica "queimadas brasil"
- **Flickr API**: Fotos geotagged no Brasil
- **YouTube**: Frames de vídeos de queimadas
- **Validation**: Manual + crosscheck com INPE

### 🛠️ Pipeline de Coleta

#### Fase 1: Automação (3 dias)
```python
# Script 1: INPE data scraper
fetch_inpe_fire_data(start_date, end_date, region="BRAZIL")

# Script 2: Satellite image downloader  
download_sentinel_images(coordinates, date_range)

# Script 3: Web scraper (responsável)
scrape_fire_images(keywords=["queimada brasil", "incendio florestal"])
```

#### Fase 2: Processamento (2 dias)
```python
# Quality filter
filter_by_resolution(min_size=(512, 512))
filter_by_quality(blur_threshold, contrast_threshold)

# Geographic validation
validate_coordinates(lat, lon, country="BR")

# Duplicate removal
remove_duplicates(hash_similarity=0.95)
```

#### Fase 3: Anotação (5 dias)
- **Tool**: Usar nossa annotation_tool.py
- **Classes**: Fire, Smoke, Clear, Vegetation, Building
- **Bounding boxes**: Para objetos pequenos
- **Segmentation masks**: Para areas grandes

### 📁 Estrutura do Dataset

```
datasets/
├── raw/
│   ├── inpe/           # Dados oficiais INPE
│   ├── satellite/      # Sentinel-2, MODIS
│   ├── web/           # Imagens coletadas da web
│   └── validation/    # Imagens para teste manual
├── processed/
│   ├── train/ (70%)   # 700 imagens
│   ├── val/ (20%)     # 200 imagens  
│   └── test/ (10%)    # 100 imagens
├── annotations/
│   ├── bbox/          # YOLO format
│   ├── masks/         # Segmentation masks
│   └── metadata.json # Labels + confidence
└── augmented/
    └── train_aug/     # Data augmentation
```

### 🎯 Targets de Qualidade

- **Resolução mínima**: 512x512 pixels
- **Diversidade geográfica**: Todos os biomas brasileiros
- **Diversidade temporal**: Diferentes épocas do ano
- **Balance**: 60% com fogo, 40% sem fogo (controle)
- **Annotation quality**: Double-check em 10% das imagens

### 🚀 Cronograma Sprint 2

**Semana 1:**
- [x] Estrutura base (feito)
- [ ] Scripts de coleta INPE + NASA
- [ ] Download inicial 200 imagens

**Semana 2:**  
- [ ] Coleta web + satellite (800 imagens)
- [ ] Processamento e limpeza
- [ ] Início da anotação

**Resultado esperado**: Dataset brasileiro pronto para training!

---

**🔥 VAMOS COM TUDO, NA RAÇA! Sem firula, só resultado!** 💪
