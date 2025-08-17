#!/usr/bin/env python3
"""
🔥 INPE Fire Data Collector
Coleta dados oficiais de queimadas do INPE - Brasil

VAI CORINTHIANS! 💪 (implementando na raça, sem firula!)
"""

import requests
import pandas as pd
import json
from datetime import datetime, timedelta
from pathlib import Path
import time
import logging

# Setup logging estilo corinthiano: direto e na raça!
logging.basicConfig(
    level=logging.INFO,
    format='🔥 %(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class INPEFireCollector:
    """Coletor oficial de dados de queimadas do INPE"""
    
    def __init__(self):
        self.base_url = "https://queimadas.dgi.inpe.br/queimadas/dados-abertos/api"
        self.output_dir = Path("../datasets/raw/inpe")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info("🚀 INPE Fire Collector iniciado - Vamos pegar os dados!")
    
    def fetch_fire_data(self, start_date: str, end_date: str, region: str = "BRAZIL"):
        """
        Coleta dados de focos de calor do INPE
        
        Args:
            start_date: "YYYY-MM-DD"
            end_date: "YYYY-MM-DD" 
            region: "BRAZIL" ou código do estado
        """
        logger.info(f"🔍 Coletando dados de {start_date} a {end_date} para {region}")
        
        # URL da API do INPE para focos de calor
        url = f"{self.base_url}/focos/"
        
        params = {
            'data_inicio': start_date,
            'data_fim': end_date,
            'formato': 'json'
        }
        
        if region != "BRAZIL":
            params['estado'] = region
            
        try:
            logger.info("📡 Fazendo request para API do INPE...")
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"✅ Coletados {len(data)} focos de calor!")
            
            # Salvar dados brutos
            output_file = self.output_dir / f"inpe_fires_{start_date}_{end_date}_{region}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"💾 Dados salvos em: {output_file}")
            return data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Erro ao acessar API do INPE: {e}")
            return None
        except Exception as e:
            logger.error(f"❌ Erro inesperado: {e}")
            return None
    
    def process_fire_data(self, fire_data: list) -> pd.DataFrame:
        """Processa dados brutos do INPE para formato utilizável"""
        logger.info("⚙️ Processando dados de queimadas...")
        
        processed_data = []
        
        for fire in fire_data:
            try:
                processed_fire = {
                    'id': fire.get('id'),
                    'latitude': float(fire.get('lat', 0)),
                    'longitude': float(fire.get('lon', 0)),
                    'data_hora': fire.get('data_hora'),
                    'satelite': fire.get('satelite'),
                    'bioma': fire.get('bioma'),
                    'estado': fire.get('estado'),
                    'municipio': fire.get('municipio'),
                    'confianca': fire.get('confianca'),
                    'frp': fire.get('frp'),  # Fire Radiative Power
                    'precipitacao': fire.get('precipitacao'),
                    'numero_dias_sem_chuva': fire.get('numero_dias_sem_chuva')
                }
                processed_data.append(processed_fire)
                
            except Exception as e:
                logger.warning(f"⚠️ Erro ao processar foco: {e}")
                continue
        
        df = pd.DataFrame(processed_data)
        logger.info(f"✅ Processados {len(df)} focos válidos")
        
        return df
    
    def get_fire_hotspots_last_30_days(self, state: str = None):
        """Coleta focos dos últimos 30 dias - dados mais recentes"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        
        region = state if state else "BRAZIL"
        
        data = self.fetch_fire_data(
            start_date.strftime("%Y-%m-%d"),
            end_date.strftime("%Y-%m-%d"),
            region
        )
        
        if data:
            df = self.process_fire_data(data)
            
            # Estatísticas corinthianas (direto ao ponto!)
            logger.info("📊 ESTATÍSTICAS DOS FOCOS:")
            logger.info(f"   🔥 Total de focos: {len(df)}")
            logger.info(f"   🌍 Estados: {df['estado'].nunique()}")
            logger.info(f"   🌳 Biomas: {df['bioma'].nunique()}")
            logger.info(f"   📡 Satélites: {df['satelite'].nunique()}")
            
            # Top 5 estados com mais focos
            top_states = df['estado'].value_counts().head()
            logger.info("🏆 TOP 5 ESTADOS COM MAIS FOCOS:")
            for state, count in top_states.items():
                logger.info(f"   {state}: {count} focos")
            
            # Salvar processado
            output_file = self.output_dir / f"processed_fires_last_30_days.csv"
            df.to_csv(output_file, index=False)
            logger.info(f"💾 Dataset processado salvo: {output_file}")
            
            return df
        
        return None
    
    def collect_historical_data(self, months_back: int = 12):
        """Coleta dados históricos para formar dataset robusto"""
        logger.info(f"📚 Coletando dados históricos de {months_back} meses")
        
        all_data = []
        end_date = datetime.now()
        
        for month in range(months_back):
            current_date = end_date - timedelta(days=30 * month)
            start_month = current_date - timedelta(days=30)
            
            logger.info(f"📅 Coletando mês: {current_date.strftime('%Y-%m')}")
            
            data = self.fetch_fire_data(
                start_month.strftime("%Y-%m-%d"),
                current_date.strftime("%Y-%m-%d"),
                "BRAZIL"
            )
            
            if data:
                all_data.extend(data)
                logger.info(f"✅ Coletados {len(data)} focos do mês")
            
            # Rate limiting - INPE é público mas vamos ser educados
            time.sleep(2)
        
        if all_data:
            logger.info(f"🎯 TOTAL COLETADO: {len(all_data)} focos históricos!")
            
            df = self.process_fire_data(all_data)
            output_file = self.output_dir / f"historical_fires_{months_back}months.csv"
            df.to_csv(output_file, index=False)
            
            logger.info(f"💾 Dataset histórico salvo: {output_file}")
            return df
        
        return None

def main():
    """Função principal - execução corinthiana! 💪"""
    logger.info("🔥🔥🔥 INICIANDO COLETA DE DADOS INPE - VAI CORINTHIANS! 🔥🔥🔥")
    
    collector = INPEFireCollector()
    
    # Coleta dados recentes primeiro
    logger.info("🚀 FASE 1: Dados dos últimos 30 dias")
    recent_data = collector.get_fire_hotspots_last_30_days()
    
    if recent_data is not None:
        logger.info("✅ Dados recentes coletados com sucesso!")
    else:
        logger.error("❌ Falha na coleta de dados recentes")
    
    # Coleta dados históricos
    logger.info("🚀 FASE 2: Dados históricos (12 meses)")
    historical_data = collector.collect_historical_data(months_back=12)
    
    if historical_data is not None:
        logger.info("✅ Dados históricos coletados com sucesso!")
    else:
        logger.error("❌ Falha na coleta de dados históricos")
    
    logger.info("🏆 COLETA FINALIZADA - AGORA É SÓ TREINAR O MODELO! 🔥")

if __name__ == "__main__":
    main()
