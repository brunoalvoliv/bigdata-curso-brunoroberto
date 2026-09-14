#!/usr/bin/env python3
"""
Avaliação Final — Etapa 2: Execução do Pipeline de Big Data
Processamento Medallion (Raw -> Bronze -> Silver -> Gold)
Base: avaliacao_transactions.csv (30.000 registros com channel e merchant_category)
Curso: Big Data para Negócios
"""
import duckdb
import os
import pandas as pd

def main():
    print("=================================================================")
    print("   ETAPA 2 — EXECUÇÃO DO PIPELINE MEDALLION DE BIG DATA (TECHPAY)")
    print("=================================================================")
    
    con = duckdb.connect()
    base_dir = "avaliacao_final/etapa2_bigdata/data"
    os.makedirs(f"{base_dir}/raw", exist_ok=True)
    os.makedirs(f"{base_dir}/bronze", exist_ok=True)
    os.makedirs(f"{base_dir}/silver", exist_ok=True)
    os.makedirs(f"{base_dir}/gold", exist_ok=True)
    
    source_csv = "data_sources/avaliacao_transactions.csv"
    if not os.path.exists(source_csv):
        source_csv = "test/avaliacao_transactions.csv"
        
    print(f"\n1. Ingestão & Tabela Raw: Carregando '{source_csv}'...")
    raw_path = f"{base_dir}/raw/avaliacao_transactions_raw.csv"
    pd.read_csv(source_csv).to_csv(raw_path, index=False)
    
    raw_count = con.sql(f"SELECT COUNT(*) FROM read_csv_auto('{raw_path}')").fetchone()[0]
    print(f"   [Raw] Registros brutos ingeridos: {raw_count} linhas.")
    
    print("\n2. Processamento da Camada Bronze (Limpeza & Sanitização)...")
    # Sanitização de nulos, remoção de valores impossíveis (amount <= 0), conversão de booleano
    con.sql(f"""
    COPY (
        SELECT DISTINCT
            CAST(transaction_id AS INT) AS transaction_id,
            CAST(customer_id AS INT) AS customer_id,
            CAST(amount AS DOUBLE) AS amount,
            LOWER(TRIM(transaction_type)) AS transaction_type,
            LOWER(TRIM(channel)) AS channel,
            LOWER(TRIM(merchant_category)) AS merchant_category,
            CAST(timestamp AS TIMESTAMP) AS timestamp,
            LOWER(TRIM(status)) AS status,
            CAST(risk_score AS DOUBLE) AS risk_score,
            COALESCE(segment, 'Standard') AS segment,
            CAST(credit_score AS INT) AS credit_score,
            CASE 
                WHEN LOWER(TRIM(CAST(is_fraud AS VARCHAR))) IN ('true', '1', 't', 'yes') THEN TRUE
                ELSE FALSE 
            END AS is_fraud
        FROM read_csv_auto('{raw_path}')
        WHERE transaction_id IS NOT NULL 
          AND amount > 0 
          AND customer_id IS NOT NULL
    ) TO '{base_dir}/bronze/bronze_transactions.parquet' (FORMAT PARQUET, OVERWRITE_OR_IGNORE 1)
    """)
    
    bronze_count = con.sql(f"SELECT COUNT(*) FROM '{base_dir}/bronze/bronze_transactions.parquet'").fetchone()[0]
    print(f"   [Bronze] Linhas sobreviventes após limpeza: {bronze_count} (Descartadas: {raw_count - bronze_count})")
    
    print("\n3. Processamento da Camada Silver (Enriquecimento & Particionamento)...")
    # Derivação de variáveis críticas de risco: hora do dia, flag de madrugada, faixa de valor
    # Incorporação das novas dimensões de risco: channel e merchant_category
    # Aplicação de particionamento físico por ano e mes
    con.sql(f"""
    COPY (
        SELECT
            transaction_id,
            customer_id,
            segment,
            credit_score,
            amount,
            CASE 
                WHEN amount < 100 THEN 'Baixo'
                WHEN amount <= 1000 THEN 'Medio'
                ELSE 'Alto'
            END AS faixa_valor,
            transaction_type,
            channel,
            merchant_category,
            timestamp,
            EXTRACT(YEAR FROM timestamp) AS ano,
            EXTRACT(MONTH FROM timestamp) AS mes,
            EXTRACT(HOUR FROM timestamp) AS hora_dia,
            CASE 
                WHEN EXTRACT(HOUR FROM timestamp) BETWEEN 0 AND 5 THEN TRUE
                ELSE FALSE
            END AS is_madrugada,
            status,
            risk_score,
            is_fraud
        FROM '{base_dir}/bronze/bronze_transactions.parquet'
    ) TO '{base_dir}/silver/silver_transactions.parquet' (FORMAT PARQUET, OVERWRITE_OR_IGNORE 1)
    """)

    # Particionamento físico Hive (ano/mes)
    con.sql(f"""
    COPY (
        SELECT * FROM '{base_dir}/silver/silver_transactions.parquet'
    ) TO '{base_dir}/silver/partitioned' (FORMAT PARQUET, PARTITION_BY (ano, mes), OVERWRITE_OR_IGNORE 1)
    """)
    
    silver_count = con.sql(f"SELECT COUNT(*) FROM '{base_dir}/silver/silver_transactions.parquet'").fetchone()[0]
    print(f"   [Silver] Linhas enriquecidas e particionadas (ano/mes) na camada Silver: {silver_count}")
    
    print("\n4. Processamento da Camada Gold (Construção das Tabelas Agregadas de BI)...")
    
    # Gold Table 1: Risco por Canal e Categoria de Estabelecimento
    con.sql(f"""
    COPY (
        SELECT
            channel,
            merchant_category,
            COUNT(*) AS total_transacoes,
            ROUND(SUM(amount), 2) AS volume_total,
            SUM(CASE WHEN is_fraud THEN 1 ELSE 0 END) AS total_fraudes,
            ROUND(SUM(CASE WHEN is_fraud THEN amount ELSE 0 END), 2) AS valor_perda_fraude,
            ROUND(SUM(CASE WHEN is_fraud THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS taxa_fraude_pct
        FROM '{base_dir}/silver/silver_transactions.parquet'
        GROUP BY channel, merchant_category
        ORDER BY taxa_fraude_pct DESC
    ) TO '{base_dir}/gold/gold_fraud_by_channel_category.parquet' (FORMAT PARQUET, OVERWRITE_OR_IGNORE 1)
    """)
    
    # Gold Table 2: Risco por Horário do Dia e Flag de Madrugada
    con.sql(f"""
    COPY (
        SELECT
            hora_dia,
            is_madrugada,
            COUNT(*) AS total_transacoes,
            ROUND(SUM(amount), 2) AS volume_total,
            SUM(CASE WHEN is_fraud THEN 1 ELSE 0 END) AS total_fraudes,
            ROUND(SUM(CASE WHEN is_fraud THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS taxa_fraude_pct
        FROM '{base_dir}/silver/silver_transactions.parquet'
        GROUP BY hora_dia, is_madrugada
        ORDER BY hora_dia
    ) TO '{base_dir}/gold/gold_hourly_risk.parquet' (FORMAT PARQUET, OVERWRITE_OR_IGNORE 1)
    """)
    
    print("   [Gold] Tabela 1: gold_fraud_by_channel_category criada com sucesso.")
    print("   [Gold] Tabela 2: gold_hourly_risk criada com sucesso.")
    
    print("\n=================================================================")
    print("   PIPELINE DA ETAPA 2 CONCLUÍDO COM SUCESSO!")
    print("=================================================================")

if __name__ == "__main__":
    main()
