#!/usr/bin/env python3
"""
Lab 04: Particionamento (Rota B - DuckDB / Parquet Particionamento)
Curso: Big Data para Negócios
"""
import duckdb
import os

def main():
    print("=== Lab 04: Particionamento por Ano/Mês (Rota B) ===")
    con = duckdb.connect()
    
    raw_tx = "bigdata/raw/transactions/transactions_synthetic.csv"
    output_partition_dir = "bigdata/partitioned_transactions"
    
    # Ingerir CSV e criar coluna de ano e mês
    con.sql(f"""
    COPY (
        SELECT 
            transaction_id,
            customer_id,
            amount,
            transaction_type,
            status,
            risk_score,
            is_fraud,
            YEAR(CAST(timestamp AS TIMESTAMP)) AS ano,
            MONTH(CAST(timestamp AS TIMESTAMP)) AS mes
        FROM read_csv_auto('{raw_tx}')
    ) TO '{output_partition_dir}' (FORMAT PARQUET, PARTITION_BY (ano, mes), OVERWRITE_OR_IGNORE 1)
    """)
    
    print(f"[OK] Dados exportados particionados em Parquet para '{output_partition_dir}'")
    
    # Consultar demonstrando Partition Pruning
    df_pruned = con.sql(f"""
    SELECT ano, mes, COUNT(*) AS total_transacoes, ROUND(SUM(amount), 2) AS volume_total
    FROM read_parquet('{output_partition_dir}/*/*/*.parquet')
    GROUP BY ano, mes
    ORDER BY ano, mes
    LIMIT 5
    """).df()
    
    print("[OK] Consulta com Partition Pruning (Amostra de Partições):")
    print(df_pruned)

if __name__ == "__main__":
    main()
