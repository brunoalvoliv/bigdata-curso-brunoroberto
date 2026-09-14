#!/usr/bin/env python3
"""
Lab 09: Exportação de Dados para BI (Rota B - DuckDB / Python)
Curso: Big Data para Negócios
"""
import duckdb
import os

def main():
    print("=== Lab 09: Exportação de Dados para BI (Rota B) ===")
    con = duckdb.connect()
    
    gold_segment_path = "bigdata/gold/gold_risk_by_segment.parquet"
    out_csv = "dia3_insights_bi/lab09_export/gold_risk_by_segment.csv"
    
    if os.path.exists(gold_segment_path):
        con.sql(f"""
        COPY (SELECT * FROM '{gold_segment_path}') 
        TO '{out_csv}' (HEADER, DELIMITER ',')
        """)
        print(f"[OK] Tabela Gold exportada com sucesso para '{out_csv}'")
    else:
        print(f"[AVISO] Arquivo {gold_segment_path} não encontrado. Execute o Lab 07 primeiro.")

if __name__ == "__main__":
    main()
