#!/usr/bin/env bash
# ------------------------------------------------------------------------------
# Lab 09: Exportação de Dados para BI
# Rota A — Hive / Shell Export
# ------------------------------------------------------------------------------

echo "=== Exportando tabelas Gold do Hive para CSV local ==="
hive -e "
USE bigdata_db;
SELECT customer_segment, total_transacoes, volume_total, ticket_medio, total_fraudes, taxa_fraude_pct
FROM gold_risk_by_segment;
" | tr '\t' ',' > dia3_insights_bi/lab09_export/gold_risk_by_segment.csv

echo "[OK] Dados exportados para dia3_insights_bi/lab09_export/gold_risk_by_segment.csv"
