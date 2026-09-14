#!/usr/bin/env python3
"""
Lab 08: Análise Exploratória de Dados (EDA) (Rota B - DuckDB / Python)
Curso: Big Data para Negócios
"""
import duckdb

def main():
    print("=== Lab 08: Análise Exploratória de Dados (EDA - Rota B) ===")
    con = duckdb.connect()
    silver_path = "bigdata/silver/silver_transactions.parquet"
    
    print("\n1. Análise de Fraude por Segmento de Cliente:")
    q1 = con.sql(f"""
    SELECT
        customer_segment,
        COUNT(*) AS total_tx,
        SUM(CASE WHEN is_fraud THEN 1 ELSE 0 END) AS fraudes,
        ROUND(SUM(CASE WHEN is_fraud THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS taxa_fraude_pct
    FROM '{silver_path}'
    GROUP BY customer_segment
    ORDER BY taxa_fraude_pct DESC
    """).df()
    print(q1)
    
    print("\n2. Concentração de Fraude no Período da Madrugada (00h às 05h):")
    q2 = con.sql(f"""
    SELECT
        is_madrugada,
        COUNT(*) AS total_tx,
        SUM(CASE WHEN is_fraud THEN 1 ELSE 0 END) AS fraudes,
        ROUND(SUM(CASE WHEN is_fraud THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS taxa_fraude_pct
    FROM '{silver_path}'
    GROUP BY is_madrugada
    """).df()
    print(q2)

if __name__ == "__main__":
    main()
