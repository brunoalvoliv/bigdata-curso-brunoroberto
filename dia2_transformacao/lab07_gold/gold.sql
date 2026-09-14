-- =============================================================================
-- Lab 07: Camada Gold — Agregar para Negócios & BI
-- Rota A — Hive SQL
-- =============================================================================

USE bigdata_db;

-- 1. Visão Agregada por Segmento do Cliente
CREATE TABLE IF NOT EXISTS gold_risk_by_segment
STORED AS PARQUET AS
SELECT
  customer_segment,
  COUNT(*) AS total_transacoes,
  SUM(amount) AS volume_total,
  ROUND(AVG(amount), 2) AS ticket_medio,
  SUM(CASE WHEN is_fraud THEN 1 ELSE 0 END) AS total_fraudes,
  ROUND(SUM(CASE WHEN is_fraud THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS taxa_fraude_pct
FROM silver_transactions
GROUP BY customer_segment;

-- 2. Visão Agregada por Período do Dia e Faixa de Valor
CREATE TABLE IF NOT EXISTS gold_risk_by_hour_faixa
STORED AS PARQUET AS
SELECT
  is_madrugada,
  faixa_valor,
  COUNT(*) AS total_transacoes,
  SUM(amount) AS volume_total,
  SUM(CASE WHEN is_fraud THEN 1 ELSE 0 END) AS total_fraudes,
  ROUND(SUM(CASE WHEN is_fraud THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS taxa_fraude_pct
FROM silver_transactions
GROUP BY is_madrugada, faixa_valor;
