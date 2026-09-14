#!/usr/bin/env bash
# ------------------------------------------------------------------------------
# Lab 02: Sqoop — Ingestão de Banco Relacional (MySQL -> HDFS)
# Rota A — Cluster Real
# ------------------------------------------------------------------------------

MYSQL_HOST="localhost"
MYSQL_DB="bigdata_course"
MYSQL_USER="root"
MYSQL_PASS="SUASENHA"

echo "=== Ingestão via Sqoop: Importando clientes ==="
sqoop import \
  --connect jdbc:mysql://${MYSQL_HOST}:3306/${MYSQL_DB} \
  --username ${MYSQL_USER} \
  --password ${MYSQL_PASS} \
  --table customers \
  --target-dir /user/bigdata/raw/customers \
  --delete-target-dir \
  --m 1 \
  --fields-terminated-by ','

echo "=== Ingestão via Sqoop: Importando transações ==="
sqoop import \
  --connect jdbc:mysql://${MYSQL_HOST}:3306/${MYSQL_DB} \
  --username ${MYSQL_USER} \
  --password ${MYSQL_PASS} \
  --table transactions \
  --target-dir /user/bigdata/raw/transactions \
  --delete-target-dir \
  --m 1 \
  --fields-terminated-by ','

echo "=== Validação dos dados no HDFS ==="
hadoop fs -ls /user/bigdata/raw/customers
hadoop fs -ls /user/bigdata/raw/transactions
