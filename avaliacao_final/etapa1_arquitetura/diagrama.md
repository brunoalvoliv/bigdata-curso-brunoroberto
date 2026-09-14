# Etapa 1 — Arquitetura de Big Data (Diagrama)

## Diagrama da Arquitetura Medallion da TechPay

```mermaid
flowchart TD
    subgraph DataSources [" Origem dos Dados (Sistemas Origem TechPay) "]
        A1["App Mobile (API / Eventos JSON)"]
        A2["Web Application (PostgreSQL / MySQL)"]
        A3["Caixas Eletronicos & POS (Logs de Terminal)"]
    end

    subgraph IngestionLayer [" Camada de Ingestao & Transporte "]
        B1["Batch: Apache Sqoop / Python Ingestor"]
        B2["Streaming: Apache Kafka (Visao Futura Real-Time)"]
    end

    subgraph RawLayer [" Camada Raw / Data Lake (Dados Brutos) "]
        C1["HDFS / Storage Object Local (/user/bigdata/raw/)<br/>Formato: CSV / JSON Bruto<br/>Sem alteracao de formato, retencao de historico completo"]
    end

    subgraph MedallionProcessing [" Camada de Processamento Medallion (Apache Spark / DuckDB) "]
        D1["Bronze Layer (Sanitizada & Unificada)<br/>Formato: Apache Parquet<br/>Remocao de nulos criticos, deduplicacao, sanitizacao de tipos"]
        
        D2["Silver Layer (Enriquecida & Relacional)<br/>Formato: Apache Parquet<br/>Particionamento: ano / mes<br/>Joins com Clientes, calculo de hora_dia, flag_madrugada, faixa_valor, combinacao channel + category"]
        
        D3["Gold Layer (Visoes Agregadas de Negocio)<br/>Formato: Apache Parquet<br/>Tabelas agregadas: Risco por Canal, Risco por Categoria, Risco por Horario/Madrugada"]
    end

    subgraph ServingBIML [" Camada de Serving, BI & Machine Learning "]
        E1["Dashboard Executivo HTML / Plotly / Metabase"]
        E2["Modelo Preditivo ML (Scikit-Learn / Spark MLlib - Deteccao de Fraude)"]
        E3["Alertas Operacionais de Bloqueio em Tempo Real"]
    end

    %% Conexoes
    A1 --> B1
    A2 --> B1
    A3 --> B1
    B1 --> C1
    C1 --> D1
    D1 --> D2
    D2 --> D3
    D3 --> E1
    D2 --> E2
    E2 --> E3
```

---

## Resumo dos Formatos e Particionamento por Camada

| Camada | Formato de Arquivo | Compressao | Estrategia de Particionamento | Justificativa Tecnica |
|---|---|---|---|---|
| **Raw** | CSV / JSON | Nenhuma / Snappy | Nenhuma (Estrutura por diretorio de origem) | Preserva a fidelidade exata do dado de origem para auditoria. |
| **Bronze** | Apache Parquet | Snappy | Nenhuma | Formato colunar otimizado para leitura veloz durante a limpeza. |
| **Silver** | Apache Parquet | Snappy | `ano` / `mes` | Permite *Partition Pruning* em consultas temporais de compliance e risco. |
| **Gold** | Apache Parquet | Snappy | `ano` (se volume for alto) ou Tabela Unica | Agregados pre-calculados de alto desempenho para dashboards executivos. |
