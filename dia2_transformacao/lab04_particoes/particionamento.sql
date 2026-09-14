-- =============================================================================
-- Lab 04: Hive — Particionamento Estático e Dinâmico
-- Rota A — Hive SQL
-- =============================================================================

USE bigdata_db;

-- 1. Habilitar Particionamento Dinâmico no Hive
SET hive.exec.dynamic.partition = true;
SET hive.exec.dynamic.partition.mode = nonstrict;

-- 2. Criar Tabela Particionada por Ano e Mês (Formato Parquet para performance)
CREATE TABLE IF NOT EXISTS transactions_partitioned (
  transaction_id INT,
  customer_id INT,
  amount FLOAT,
  transaction_type STRING,
  status STRING,
  risk_score FLOAT,
  is_fraud STRING
)
PARTITIONED BY (ano INT, mes INT)
STORED AS PARQUET;

-- 3. Inserir dados na Tabela Particionada a partir da tabela Raw
INSERT OVERWRITE TABLE transactions_partitioned PARTITION (ano, mes)
SELECT
  transaction_id,
  customer_id,
  amount,
  transaction_type,
  status,
  risk_score,
  is_fraud,
  YEAR(timestamp) AS ano,
  MONTH(timestamp) AS mes
FROM raw_transactions;

-- 4. Exemplo de Pruning (Filtro por Partição — Lê apenas a pasta correspondente)
SELECT COUNT(*) FROM transactions_partitioned WHERE ano = 2025 AND mes = 6;
SHOW PARTITIONS transactions_partitioned;
