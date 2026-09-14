-- =============================================================================
-- Lab 08: EDA — Consultas Analíticas e Insights de Negócio
-- Rota A — Hive SQL
-- =============================================================================

USE bigdata_db;

-- 1. Distribuição de Fraude por Segmento de Cliente
SELECT
  customer_segment,
  COUNT(*) AS total_tx,
  SUM(CASE WHEN is_fraud THEN 1 ELSE 0 END) AS fraudes,
  ROUND(SUM(CASE WHEN is_fraud THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS taxa_fraude_pct
FROM silver_transactions
GROUP BY customer_segment
ORDER BY taxa_fraude_pct DESC;

-- 2. Concentração de Fraude na Madrugada (00h às 05h)
SELECT
  is_madrugada,
  COUNT(*) AS total_tx,
  SUM(CASE WHEN is_fraud THEN 1 ELSE 0 END) AS fraudes,
  ROUND(SUM(CASE WHEN is_fraud THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS taxa_fraude_pct
FROM silver_transactions
GROUP BY is_madrugada;

-- 3. Top 10 Clientes com Maior Volume de Fraudes
SELECT
  customer_id,
  customer_name,
  customer_segment,
  COUNT(*) AS total_transacoes,
  SUM(CASE WHEN is_fraud THEN 1 ELSE 0 END) AS total_fraudes,
  SUM(amount) AS volume_total
FROM silver_transactions
WHERE is_fraud = TRUE
GROUP BY customer_id, customer_name, customer_segment
ORDER BY total_fraudes DESC, volume_total DESC
LIMIT 10;
