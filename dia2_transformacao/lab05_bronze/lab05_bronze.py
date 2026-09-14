#!/usr/bin/env python3
"""
Lab 05: Camada Bronze (Rota B - DuckDB / Python)
Limpeza, Deduplicação e Sanitização de Tipos
Curso: Big Data para Negócios
"""
import duckdb
import os

def main():
    print("=== Lab 05: Processamento da Camada Bronze (Rota B) ===")
    con = duckdb.connect()
    
    os.makedirs("bigdata/bronze", exist_ok=True)
    
    raw_customers_path = "bigdata/raw/customers/customers_synthetic.csv"
    raw_transactions_path = "bigdata/raw/transactions/transactions_synthetic.csv"
    
    # 1. Processar Bronze Customers
    con.sql(f"""
    COPY (
        SELECT DISTINCT
            CAST(customer_id AS INT) AS customer_id,
            TRIM(name) AS name,
            regexp_replace(cpf, '[^0-9]', '', 'g') AS cpf_clean,
            LOWER(TRIM(email)) AS email,
            COALESCE(segment, 'Standard') AS segment,
            CAST(credit_score AS INT) AS credit_score,
            CAST(created_at AS DATE) AS created_at
        FROM read_csv_auto('{raw_customers_path}')
        WHERE customer_id IS NOT NULL
    ) TO 'bigdata/bronze/bronze_customers.parquet' (FORMAT PARQUET, OVERWRITE_OR_IGNORE 1)
    """)
    
    # 2. Processar Bronze Transactions
    con.sql(f"""
    COPY (
        SELECT DISTINCT
            CAST(transaction_id AS INT) AS transaction_id,
            CAST(customer_id AS INT) AS customer_id,
            CAST(amount AS DOUBLE) AS amount,
            LOWER(TRIM(transaction_type)) AS transaction_type,
            CAST(timestamp AS TIMESTAMP) AS timestamp,
            LOWER(TRIM(status)) AS status,
            CAST(risk_score AS DOUBLE) AS risk_score,
            CASE 
                WHEN LOWER(TRIM(CAST(is_fraud AS VARCHAR))) IN ('true', '1', 't', 'yes') THEN TRUE
                ELSE FALSE 
            END AS is_fraud
        FROM read_csv_auto('{raw_transactions_path}')
        WHERE transaction_id IS NOT NULL AND amount > 0
    ) TO 'bigdata/bronze/bronze_transactions.parquet' (FORMAT PARQUET, OVERWRITE_OR_IGNORE 1)
    """)
    
    c_count = con.sql("SELECT COUNT(*) FROM 'bigdata/bronze/bronze_customers.parquet'").fetchone()[0]
    t_count = con.sql("SELECT COUNT(*) FROM 'bigdata/bronze/bronze_transactions.parquet'").fetchone()[0]
    
    print(f"[OK] Camada Bronze criada com sucesso!")
    print(f"  - Clientes Bronze: {c_count} registros")
    print(f"  - Transações Bronze: {t_count} registros")

if __name__ == "__main__":
    main()
