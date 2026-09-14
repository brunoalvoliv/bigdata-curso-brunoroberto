#!/usr/bin/env python3
"""
Lab 02: Sqoop — Ingestão de Banco Relacional (Rota B - SQLite/DuckDB)
Curso: Big Data para Negócios
"""
import sqlite3
import pandas as pd
import duckdb
import os

def main():
    print("=== Lab 02: Ingestão de Banco Relacional (Rota B) ===")
    
    # 1. Simular Banco Relacional de Origem com SQLite
    db_path = "bigdata_course.db"
    conn = sqlite3.connect(db_path)
    
    # Carregar CSVs de origem no SQLite
    customers_df = pd.read_csv("data_sources/customers_synthetic.csv")
    transactions_df = pd.read_csv("data_sources/transactions_synthetic.csv")
    
    customers_df.to_sql("customers", conn, if_exists="replace", index=False)
    transactions_df.to_sql("transactions", conn, if_exists="replace", index=False)
    print("[OK] Banco relacional SQLite preenchido com tabelas 'customers' e 'transactions'.")
    
    # 2. Executar ingestão do banco para o ambiente de Big Data (DuckDB / Filesystem Raw)
    duck_con = duckdb.connect()
    
    os.makedirs("bigdata/raw/customers", exist_ok=True)
    os.makedirs("bigdata/raw/transactions", exist_ok=True)
    
    # Exportar tabelas do SQLite para arquivos no HDFS/Raw equivalente
    c_extracted = pd.read_sql_query("SELECT * FROM customers", conn)
    t_extracted = pd.read_sql_query("SELECT * FROM transactions", conn)
    
    c_extracted.to_csv("bigdata/raw/customers/customers_synthetic.csv", index=False)
    t_extracted.to_csv("bigdata/raw/transactions/transactions_synthetic.csv", index=False)
    
    print("[OK] Ingestão relacional concluída para a camada Raw.")
    print(f"Total de Clientes Ingeridos: {len(c_extracted)}")
    print(f"Total de Transações Ingeridas: {len(t_extracted)}")
    
    conn.close()

if __name__ == "__main__":
    main()
