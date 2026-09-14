# Estrutura do Repositório — Big Data para Negócios

**Curso:** Big Data para Negócios  
**Instituição:** UFC / MPCE  
**Professor Responsável:** Luiz Alexandre Moreira Barros  
**Aluno(s):** Bruno Alves de Oliveira e Roberto  
**Repositório:** `bigdata-curso-brunoroberto`  

---

## Mapeamento Completo da Estrutura de Pastas e Arquivos

Este repositório centraliza 100% dos **12 Laboratórios** (30% da nota) e das **4 Etapas da Avaliação Final** (70% da nota + bônus de ML), organizados estritamente conforme a especificação do curso:

```text
bigdata-curso-brunoroberto/
├── README.md                        <- Visão geral e guia rápido do repositório
├── 00_ESTRUTURA_REPOSITORIO.md      <- Mapeamento completo e convenção de pastas do projeto
├── COMO_VISUALIZAR_DASHBOARD.md     <- Guia de execução local do Dashboard em http://localhost:8000
├── servir_dashboard.py              <- Servidor HTTP auxiliar Python para abertura do Dashboard
├── .gitignore                       <- Regras de exclusão de datasets grandes (.csv, .parquet, cache)
│
├── dia1_fundamentos/                <- Módulo 1: Fundamentos de Arquitetura Distributed & Ingestão
│   ├── lab01_hdfs/                  <- Lab 01: HDFS - Arquitetura em camadas e replicação 3x
│   │   ├── comandos.sh              <- Scripts de shell para Rota A (Cluster Real Hadoop)
│   │   └── lab01_hdfs.py            <- Script Python de simulação HDFS para Rota B (Local)
│   └── lab02_sqoop/                 <- Lab 02: Sqoop - Ingestão relacional para Data Lake
│       ├── import.sh                <- Ingestão relacional MySQL/SQLite em batch
│       └── lab02_sqoop.py           <- Ingestão relacional simulada via DuckDB/SQLite
│
├── dia2_transformacao/              <- Módulo 2: Processamento Medallion & Engenharia de Dados
│   ├── lab03_hive_tabelas/          <- Lab 03: Hive - Tabelas Managed vs External (Drop behavior)
│   │   ├── create_tables.sql
│   │   └── lab03_hive.py
│   ├── lab04_particoes/             <- Lab 04: Hive - Particionamento Estático e Dinâmico por ano/mês
│   │   ├── particionamento.sql
│   │   └── lab04_particoes.py
│   ├── lab05_bronze/                <- Lab 05: Camada Bronze - Sanitização, deduplicação e limpeza
│   │   ├── bronze.sql
│   │   └── lab05_bronze.py
│   ├── lab06_silver/                <- Lab 06: Camada Silver - Enriquecimento e engenharia de atributos
│   │   ├── silver.sql
│   │   └── lab06_silver.py
│   ├── lab07_gold/                  <- Lab 07: Camada Gold - Tabelas agregadas orientadas a BI
│   │   ├── gold.sql
│   │   └── lab07_gold.py
│   └── lab08_eda/                   <- Lab 08: Análise Exploratória de Dados (EDA Queries)
│       ├── eda_queries.sql
│       └── lab08_eda.py
│
├── dia3_insights_bi/                <- Módulo 3: Distribuição, BI & Machine Learning
│   ├── lab09_export/                <- Lab 09: Exportação de dados para consumo em BI
│   │   ├── export.sh
│   │   └── lab09_export.py
│   ├── lab10_spark/                 <- Lab 10: Processamento Distribuído com PySpark
│   │   └── spark_queries.py
│   ├── lab11_dashboard/             <- Lab 11: Geração de Dashboard HTML interativo
│   │   ├── dashboard.py
│   │   └── dashboard_fraude.html
│   └── lab12_ml_preview/            <- Lab 12: Modelo Preditivo de Fraude (Preview ML)
│       └── modelo_fraude.py
│
└── avaliacao_final/                 <- PROJETO FINAL (70% DA NOTA + BÔNUS)
    ├── RELATORIO_AVALIACAO_FINAL.md <- Relatório Consolidado Master (Visão Unificada em Prosa)
    │
    ├── etapa1_arquitetura/          <- Etapa 1: Arquitetura de Big Data & Justificativa (15%)
    │   ├── diagrama.md              <- Fluxograma da Arquitetura Medallion (Mermaid + Tabela Formatos)
    │   └── justificativa.md         <- Relatório explicativo das 4 perguntas técnicas
    │
    ├── etapa2_bigdata/              <- Etapa 2: Execução de Pipeline Medallion em 30.000 txs (30%)
    │   ├── pipeline.py              <- Pipeline completo em Python/DuckDB (Raw -> Bronze -> Silver -> Gold)
    │   └── explicacao.md            <- Relatório em prosa explicativa (sem código colado)
    │
    ├── etapa3_analise/              <- Etapa 3: Análise de Negócio & Dashboard Executivo (25%)
    │   ├── analises.py              <- Queries analíticas de risco por canal, categoria, horário e segmento
    │   ├── generate_dashboard.py    <- Gerador do Dashboard HTML Executivo
    │   ├── servir_dashboard.py      <- Servidor local HTTP para testes em localhost:8000
    │   ├── dashboard.html           <- Dashboard Interativo HTML5 / Plotly.js
    │   └── ideia_bi.md              <- Descrição do BI como produto + Framework Finding -> Insight -> Ação
    │
    └── etapa4_ml/                   <- Etapa 4: Modelo Preditivo de Fraude (Bônus de ML)
        ├── modelo_fraude.py         <- Regressão Logística com StandardScaler e Class Weight
        └── explicacao.md            <- Relatório de métricas (ROC-AUC 0.7292) e coeficientes
```

---

## Ambiente Técnico Utilizado

O projeto foi configurado com suporte 100% à **Rota B (Sem Admin / Local)**:
- **Linguagem:** Python 3.9+
- **Motor Analítico SQL:** DuckDB (execução nativa de SQL sobre arquivos Apache Parquet)
- **Engine Distribuída:** PySpark Local
- **Modelagem Preditiva:** Scikit-Learn (`StandardScaler`, `LogisticRegression`)
- **Visualização Executiva:** Plotly.js + HTML5 / CSS dark mode autonomo

---

## Como Executar o Projeto

### 1. Executar qualquer Laboratório (1 a 12)
Navegue até a pasta do lab correspondente e execute o script `.py` (Rota B) ou `.sh`/`.sql` (Rota A):
```bash
python dia1_fundamentos/lab01_hdfs/lab01_hdfs.py
python dia2_transformacao/lab05_bronze/lab05_bronze.py
python dia3_insights_bi/lab11_dashboard/dashboard.py
```

### 2. Executar a Avaliação Final (Etapas 2, 3 e 4)
```bash
# 1. Executar o Pipeline Medallion (Etapa 2)
python avaliacao_final/etapa2_bigdata/pipeline.py

# 2. Executar as Análises de Negócio e Gerar o Dashboard (Etapa 3)
python avaliacao_final/etapa3_analise/analises.py
python avaliacao_final/etapa3_analise/generate_dashboard.py

# 3. Executar o Modelo Preditivo de Machine Learning (Etapa 4)
python avaliacao_final/etapa4_ml/modelo_fraude.py
```

### 3. Abrir o Dashboard Executivo no Navegador
Para abrir o Dashboard Executivo interativo em `http://localhost:8000`:
```bash
python servir_dashboard.py
```

---

## Entrega Final

Conforme a orientação da regra de entrega, o projeto é entregue através do **link único do repositório Git**:
- **Repositório:** `https://github.com/brunoalvoliv/bigdata-curso-brunoroberto.git`
