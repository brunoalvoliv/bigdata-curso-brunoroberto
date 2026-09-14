-- =============================================================================
-- Lab 06: Camada Silver — Enriquecimento e Joins
-- Rota A — Hive SQL
-- =============================================================================

USE bigdata_db;

CREATE TABLE IF NOT EXISTS silver_transactions
STORED AS PARQUET AS
SELECT
  t.transaction_id,
  t.customer_id,
  c.name AS customer_name,
  c.segment AS customer_segment,
  c.credit_score,
  t.amount,
  CASE
    WHEN t.amount < 100 THEN 'Baixo'
    WHEN t.amount <= 1000 THEN 'Medio'
    ELSE 'Alto'
  END AS faixa_valor,
  t.transaction_type,
  t.timestamp,
  HOUR(t.timestamp) AS hora_dia,
  CASE
    WHEN HOUR(t.timestamp) BETWEEN 0 AND 5 THEN TRUE
    ELSE FALSE
  END AS is_madrugada,
  t.status,
  t.risk_score,
  t.is_fraud
FROM bronze_transactions t
LEFT JOIN bronze_customers c ON t.customer_id = c.customer_id;
