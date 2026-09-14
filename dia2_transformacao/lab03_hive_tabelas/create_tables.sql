-- =============================================================================
-- Lab 03: Hive — Tabelas Managed vs External
-- Rota A — Hive SQL
-- =============================================================================

CREATE DATABASE IF NOT EXISTS bigdata_db;
USE bigdata_db;

-- 1. Criar Tabela EXTERNAL sobre os dados de Clientes da camada Raw
CREATE EXTERNAL TABLE IF NOT EXISTS raw_customers (
  customer_id INT,
  name STRING,
  cpf STRING,
  email STRING,
  segment STRING,
  credit_score INT,
  created_at STRING
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/user/bigdata/raw/customers'
TBLPROPERTIES ('skip.header.line.count'='1');

-- 2. Criar Tabela EXTERNAL sobre os dados de Transações da camada Raw
CREATE EXTERNAL TABLE IF NOT EXISTS raw_transactions (
  transaction_id INT,
  customer_id INT,
  amount FLOAT,
  transaction_type STRING,
  timestamp STRING,
  status STRING,
  risk_score FLOAT,
  is_fraud STRING
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/user/bigdata/raw/transactions'
TBLPROPERTIES ('skip.header.line.count'='1');

-- 3. Demonstração de Tabela MANAGED
CREATE TABLE IF NOT EXISTS teste_managed (
  id INT,
  valor STRING
);

INSERT INTO teste_managed VALUES (1, 'Linha de teste Managed');

-- Experimento DROP:
-- DROP TABLE teste_managed;    -- Apaga dados no HDFS (/user/hive/warehouse/teste_managed)
-- DROP TABLE raw_customers;    -- Apaga apenas os metadados no Hive metastore; mantém o arquivo no HDFS!
