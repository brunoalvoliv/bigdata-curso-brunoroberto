-- =============================================================================
-- Lab 05: Camada Bronze — Limpeza, Deduplicação e Sanitização
-- Rota A — Hive SQL
-- =============================================================================

USE bigdata_db;

-- 1. Tabela Bronze para Clientes
CREATE TABLE IF NOT EXISTS bronze_customers
STORED AS PARQUET AS
SELECT DISTINCT
  CAST(customer_id AS INT) AS customer_id,
  TRIM(name) AS name,
  REGEXP_REPLACE(cpf, '[^0-9]', '') AS cpf_clean,
  LOWER(TRIM(email)) AS email,
  COALESCE(segment, 'Standard') AS segment,
  CAST(credit_score AS INT) AS credit_score,
  CAST(created_at AS DATE) AS created_at
FROM raw_customers
WHERE customer_id IS NOT NULL;

-- 2. Tabela Bronze para Transações
CREATE TABLE IF NOT EXISTS bronze_transactions
STORED AS PARQUET AS
SELECT DISTINCT
  CAST(transaction_id AS INT) AS transaction_id,
  CAST(customer_id AS INT) AS customer_id,
  CAST(amount AS DOUBLE) AS amount,
  LOWER(TRIM(transaction_type)) AS transaction_type,
  CAST(timestamp AS TIMESTAMP) AS timestamp,
  LOWER(TRIM(status)) AS status,
  CAST(risk_score AS DOUBLE) AS risk_score,
  CASE
    WHEN LOWER(TRIM(is_fraud)) IN ('true', '1', 't', 'yes') THEN TRUE
    ELSE FALSE
  END AS is_fraud
FROM raw_transactions
WHERE transaction_id IS NOT NULL AND amount > 0;
