#!/usr/bin/env python3
"""
🔥 Teste do INPE Fire Data Collector
Execução corinthiana! 💪
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from scripts.collect_inpe_data import INPEFireCollector
import logging

def test_collector():
    """Testa o coletor INPE com dados pequenos primeiro"""
    print("🔥" * 50)
    print("🚀 TESTANDO COLETOR INPE - VAI CORINTHIANS! 💪")
    print("🔥" * 50)
    
    collector = INPEFireCollector()
    
    # Teste 1: Dados de 1 semana
    print("\n📅 TESTE 1: Coletando dados da última semana...")
    try:
        from datetime import datetime, timedelta
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        
        data = collector.fetch_fire_data(
            start_date.strftime("%Y-%m-%d"),
            end_date.strftime("%Y-%m-%d"),
            "SP"  # São Paulo primeiro, para testar
        )
        
        if data:
            print(f"✅ Sucesso! Coletados {len(data)} focos em SP")
            
            # Processar dados
            df = collector.process_fire_data(data)
            print(f"✅ Processados {len(df)} focos válidos")
            
            # Mostrar amostra
            if len(df) > 0:
                print("\n📊 AMOSTRA DOS DADOS:")
                print(df.head())
                print(f"\n🏆 Colunas: {list(df.columns)}")
            else:
                print("⚠️ Nenhum foco encontrado em SP na última semana")
        else:
            print("❌ Falha na coleta")
            
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
    
    print("\n🏁 TESTE FINALIZADO!")

if __name__ == "__main__":
    test_collector()
