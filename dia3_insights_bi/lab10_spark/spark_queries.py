#!/usr/bin/env python3
"""
Lab 10: Processamento Distribuído com PySpark
Curso: Big Data para Negócios
"""
import os

try:
    from pyspark.sql import SparkSession
    from pyspark.sql import functions as F
    HAS_PYSPARK = True
except ImportError:
    HAS_PYSPARK = False

import duckdb

def main():
    print("=== Lab 10: Processamento com PySpark ===")
    
    if HAS_PYSPARK:
        spark = SparkSession.builder \
            .appName("Lab10_Spark_Queries") \
            .master("local[*]") \
            .getOrCreate()
        
        silver_path = "bigdata/silver/silver_transactions.parquet"
        if os.path.exists(silver_path):
            df = spark.read.parquet(silver_path)
            print(f"[PySpark] Total de registros na Silver: {df.count()}")
            
            # Análise agregada via DataFrame API
            df_agg = df.groupBy("customer_segment") \
                .agg(
                    F.count("*").alias("total_tx"),
                    F.sum(F.when(F.col("is_fraud") == True, 1).otherwise(0)).alias("total_fraudes"),
                    F.round(F.avg("amount"), 2).alias("ticket_medio")
                )
            df_agg.show()
        else:
            print(f"[AVISO] Parquet Silver não encontrado em {silver_path}")
        spark.stop()
    else:
        print("[INFO] PySpark não instalado no ambiente local. Executando simulação analítica equivalente com DuckDB:")
        con = duckdb.connect()
        silver_path = "bigdata/silver/silver_transactions.parquet"
        if os.path.exists(silver_path):
            res = con.sql(f"""
            SELECT 
                customer_segment,
                COUNT(*) AS total_tx,
                SUM(CASE WHEN is_fraud THEN 1 ELSE 0 END) AS total_fraudes,
                ROUND(AVG(amount), 2) AS ticket_medio
            FROM '{silver_path}'
            GROUP BY customer_segment
            """).df()
            print(res)

if __name__ == "__main__":
    main()
