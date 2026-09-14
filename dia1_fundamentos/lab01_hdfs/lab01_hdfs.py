#!/usr/bin/env python3
"""
Lab 01: HDFS — Organização Local em Camadas (Rota B)
Curso: Big Data para Negócios
"""
import os
import shutil
import pandas as pd

def main():
    print("=== Lab 01: HDFS (Rota B - Organização Local) ===")
    
    # 1. Criar estrutura de camadas
    directories = [
        "bigdata/raw/customers",
        "bigdata/raw/transactions",
        "bigdata/raw/fraud_labels",
        "bigdata/bronze",
        "bigdata/silver",
        "bigdata/gold",
        "bigdata/_replica_demo"
    ]
    for d in directories:
        os.makedirs(d, exist_ok=True)
    print("[OK] Estrutura de diretórios criada.")

    # 2. Copiar datasets
    sources = {
        "data_sources/customers_synthetic.csv": "bigdata/raw/customers/customers_synthetic.csv",
        "data_sources/transactions_synthetic.csv": "bigdata/raw/transactions/transactions_synthetic.csv",
        "data_sources/fraud_labels.csv": "bigdata/raw/fraud_labels/fraud_labels.csv"
    }
    for src, dst in sources.items():
        if os.path.exists(src):
            shutil.copy(src, dst)
            print(f"Copiado {src} -> {dst}")

    # 3. Simulação de replicação (3x)
    tx_src = "bigdata/raw/transactions/transactions_synthetic.csv"
    if os.path.exists(tx_src):
        for i in range(1, 4):
            shutil.copy(tx_src, f"bigdata/_replica_demo/copia_{i}.csv")
        print("[OK] Simulação de replicação 3x concluída em bigdata/_replica_demo/")

    # 4. Contagem de linhas
    if os.path.exists("bigdata/raw/customers/customers_synthetic.csv"):
        c = pd.read_csv("bigdata/raw/customers/customers_synthetic.csv")
        t = pd.read_csv("bigdata/raw/transactions/transactions_synthetic.csv")
        f = pd.read_csv("bigdata/raw/fraud_labels/fraud_labels.csv")
        print(f"Total de Clientes: {len(c)}")
        print(f"Total de Transações: {len(t)}")
        print(f"Total de Rótulos de Fraude: {len(f)}")

if __name__ == "__main__":
    main()
