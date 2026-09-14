#!/usr/bin/env bash
# ------------------------------------------------------------------------------
# Lab 01: HDFS - Estrutura de Camadas, Upload e Replicação 3x
# Rota A — Cluster Real Hadoop
# ------------------------------------------------------------------------------

echo "=== Passo 1: Verificar daemons do Hadoop ==="
jps

echo "=== Passo 2: Criar estrutura de camadas Medallion no HDFS ==="
hadoop fs -mkdir -p /user/bigdata/raw/customers
hadoop fs -mkdir -p /user/bigdata/raw/transactions
hadoop fs -mkdir -p /user/bigdata/raw/fraud_labels
hadoop fs -mkdir -p /user/bigdata/bronze
hadoop fs -mkdir -p /user/bigdata/silver
hadoop fs -mkdir -p /user/bigdata/gold

echo "=== Passo 3: Conferir a estrutura criada ==="
hadoop fs -ls -R /user/bigdata

echo "=== Passo 4: Upload dos 3 datasets sintéticos ==="
hadoop fs -put data_sources/customers_synthetic.csv /user/bigdata/raw/customers/
hadoop fs -put data_sources/transactions_synthetic.csv /user/bigdata/raw/transactions/
hadoop fs -put data_sources/fraud_labels.csv /user/bigdata/raw/fraud_labels/

echo "=== Passo 5: Verificação de Replicação (fsck) ==="
hdfs fsck /user/bigdata/raw/transactions/transactions_synthetic.csv -files -blocks -locations

echo "=== Passo 6: Validação e Contagem de Linhas ==="
hadoop fs -cat /user/bigdata/raw/customers/*.csv | wc -l
hadoop fs -cat /user/bigdata/raw/transactions/*.csv | wc -l
hadoop fs -cat /user/bigdata/raw/fraud_labels/*.csv | wc -l
