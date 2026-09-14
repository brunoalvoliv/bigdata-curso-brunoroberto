#!/usr/bin/env python3
"""
Lab 03: Hive — Tabelas Managed vs External (Rota B - DuckDB / Python)
Curso: Big Data para Negócios
"""
import os
import pandas as pd

try:
    import duckdb
    HAS_DUCKDB = True
except ImportError:
    HAS_DUCKDB = False

def main():
    print("=== Lab 03: Hive (Tabelas Managed vs External - Rota B) ===")
    raw_customers_path = "bigdata/raw/customers/customers_synthetic.csv"
    
    if HAS_DUCKDB:
        con = duckdb.connect()
        # "External Table" equivalente (View sobre CSV)
        con.sql(f"""
        CREATE VIEW raw_customers AS
        SELECT * FROM read_csv_auto('{raw_customers_path}')
        """)
        
        count = con.sql("SELECT COUNT(*) FROM raw_customers").fetchone()[0]
        print(f"[OK] View 'raw_customers' (External) criada com {count} registros.")
        
        # "Managed Table" equivalente (Tabela interna no DuckDB)
        con.sql("CREATE TABLE teste_managed AS SELECT * FROM raw_customers LIMIT 5")
        con.sql("DROP TABLE teste_managed")
        
        file_exists = os.path.exists(raw_customers_path)
        print(f"[OK] Tabela 'teste_managed' descartada. O arquivo CSV original ainda existe? {file_exists}")
    else:
        print(f"[INFO] Processando com Pandas...")
        df = pd.read_csv(raw_customers_path)
        print(f"[OK] Leitura External de '{raw_customers_path}': {len(df)} linhas.")

if __name__ == "__main__":
    main()
