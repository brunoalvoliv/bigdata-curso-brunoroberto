#!/usr/bin/env python3
"""
Lab 07: Camada Gold (Rota B - DuckDB / Python)
Tabelas Agregadas de Negócio e BI
Curso: Big Data para Negócios
"""
import duckdb
import os

def main():
    print("=== Lab 07: Processamento da Camada Gold (Rota B) ===")
    con = duckdb.connect()
    
    os.makedirs("bigdata/gold", exist_ok=True)
    silver_path = "bigdata/silver/silver_transactions.parquet"
    
    # 1. Tabela Gold: Risco por Segmento
    con.sql(f"""
    COPY (
        SELECT
            customer_segment,
            COUNT(*) AS total_transacoes,
            ROUND(SUM(amount), 2) AS volume_total,
            ROUND(AVG(amount), 2) AS ticket_medio,
            SUM(CASE WHEN is_fraud THEN 1 ELSE 0 END) AS total_fraudes,
            ROUND(SUM(CASE WHEN is_fraud THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS taxa_fraude_pct
        FROM '{silver_path}'
        GROUP BY customer_segment
    ) TO 'bigdata/gold/gold_risk_by_segment.parquet' (FORMAT PARQUET, OVERWRITE_OR_IGNORE 1)
    """)
    
    # 2. Tabela Gold: Risco por Horário e Faixa de Valor
    con.sql(f"""
    COPY (
        SELECT
            is_madrugada,
            faixa_valor,
            COUNT(*) AS total_transacoes,
            ROUND(SUM(amount), 2) AS volume_total,
            SUM(CASE WHEN is_fraud THEN 1 ELSE 0 END) AS total_fraudes,
            ROUND(SUM(CASE WHEN is_fraud THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS taxa_fraude_pct
        FROM '{silver_path}'
        GROUP BY is_madrugada, faixa_valor
    ) TO 'bigdata/gold/gold_risk_by_hour_faixa.parquet' (FORMAT PARQUET, OVERWRITE_OR_IGNORE 1)
    """)
    
    print("[OK] Camada Gold criada com sucesso!")
    print("\n--- Amostra: Gold Risco por Segmento ---")
    print(con.sql("SELECT * FROM 'bigdata/gold/gold_risk_by_segment.parquet'").df())

if __name__ == "__main__":
    main()
