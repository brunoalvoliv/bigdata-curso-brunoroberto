#!/usr/bin/env python3
"""
Avaliação Final — Etapa 3: Análises de Negócio (EDA na Camada Gold/Silver)
Curso: Big Data para Negócios
"""
import duckdb
import pandas as pd

def main():
    print("=================================================================")
    print("   ETAPA 3 — ANÁLISES DE NEGÓCIO E RISK INSIGHTS (TECHPAY)")
    print("=================================================================")
    
    con = duckdb.connect()
    silver_path = "avaliacao_final/etapa2_bigdata/data/silver/silver_transactions.parquet"
    
    # 1. Análise de Risco por Canal (channel)
    print("\n--- 1. Taxa de Fraude por Canal de Captura ---")
    df_channel = con.sql(f"""
    SELECT
        channel,
        COUNT(*) AS total_tx,
        SUM(CASE WHEN is_fraud THEN 1 ELSE 0 END) AS total_fraudes,
        ROUND(SUM(CASE WHEN is_fraud THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS taxa_fraude_pct
    FROM '{silver_path}'
    GROUP BY channel
    ORDER BY taxa_fraude_pct DESC
    """).df()
    print(df_channel.to_string(index=False))
    
    # 2. Análise de Risco por Categoria (merchant_category)
    print("\n--- 2. Taxa de Fraude por Categoria de Estabelecimento ---")
    df_cat = con.sql(f"""
    SELECT
        merchant_category,
        COUNT(*) AS total_tx,
        SUM(CASE WHEN is_fraud THEN 1 ELSE 0 END) AS total_fraudes,
        ROUND(SUM(CASE WHEN is_fraud THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS taxa_fraude_pct
    FROM '{silver_path}'
    GROUP BY merchant_category
    ORDER BY taxa_fraude_pct DESC
    """).df()
    print(df_cat.to_string(index=False))
    
    # 3. Análise da Combinação Crítica: Canal APP + Categoria VIAGEM na Madrugada
    print("\n--- 3. Análise Combinada: Canal APP + Categoria VIAGEM + Período Madrugada ---")
    df_comb = con.sql(f"""
    SELECT
        channel,
        merchant_category,
        is_madrugada,
        COUNT(*) AS total_tx,
        SUM(CASE WHEN is_fraud THEN 1 ELSE 0 END) AS total_fraudes,
        ROUND(SUM(CASE WHEN is_fraud THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS taxa_fraude_pct
    FROM '{silver_path}'
    WHERE channel = 'app' AND merchant_category = 'viagem'
    GROUP BY channel, merchant_category, is_madrugada
    ORDER BY is_madrugada DESC
    """).df()
    print(df_comb.to_string(index=False))

    # 4. Análise por Segmento de Cliente
    print("\n--- 4. Taxa de Fraude por Segmento de Cliente ---")
    df_seg = con.sql(f"""
    SELECT
        segment,
        COUNT(*) AS total_tx,
        SUM(CASE WHEN is_fraud THEN 1 ELSE 0 END) AS total_fraudes,
        ROUND(SUM(CASE WHEN is_fraud THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS taxa_fraude_pct
    FROM '{silver_path}'
    GROUP BY segment
    ORDER BY taxa_fraude_pct DESC
    """).df()
    print(df_seg.to_string(index=False))
    
    print("\n=================================================================")
    print("   ANÁLISES DA ETAPA 3 CONCLUÍDAS COM SUCESSO!")
    print("=================================================================")

if __name__ == "__main__":
    main()
