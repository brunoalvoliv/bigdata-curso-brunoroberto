#!/usr/bin/env python3
"""
Lab 06: Camada Silver (Rota B - DuckDB / Python)
Enriquecimento de Dados, Feature Engineering e Joins
Curso: Big Data para Negócios
"""
import duckdb
import os

def main():
    print("=== Lab 06: Processamento da Camada Silver (Rota B) ===")
    con = duckdb.connect()
    
    os.makedirs("bigdata/silver", exist_ok=True)
    
    bronze_c_path = "bigdata/bronze/bronze_customers.parquet"
    bronze_t_path = "bigdata/bronze/bronze_transactions.parquet"
    
    con.sql(f"""
    COPY (
        SELECT
            t.transaction_id,
            t.customer_id,
            c.name AS customer_name,
            c.segment AS customer_segment,
            c.credit_score,
            t.amount,
            CASE 
                WHEN t.amount < 100 THEN 'Baixo'
                WHEN t.amount <= 1000 THEN 'Medio'
                ELSE 'Alto'
            END AS faixa_valor,
            t.transaction_type,
            t.timestamp,
            EXTRACT(HOUR FROM t.timestamp) AS hora_dia,
            CASE 
                WHEN EXTRACT(HOUR FROM t.timestamp) BETWEEN 0 AND 5 THEN TRUE
                ELSE FALSE
            END AS is_madrugada,
            t.status,
            t.risk_score,
            t.is_fraud
        FROM '{bronze_t_path}' t
        LEFT JOIN '{bronze_c_path}' c ON t.customer_id = c.customer_id
    ) TO 'bigdata/silver/silver_transactions.parquet' (FORMAT PARQUET, OVERWRITE_OR_IGNORE 1)
    """)
    
    s_count = con.sql("SELECT COUNT(*) FROM 'bigdata/silver/silver_transactions.parquet'").fetchone()[0]
    print(f"[OK] Camada Silver gerada com sucesso: {s_count} registros enriquecidos.")

if __name__ == "__main__":
    main()
