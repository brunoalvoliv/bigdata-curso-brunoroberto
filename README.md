# Big Data para Negocios — Repositorio de Atividades e Avaliacao Final

**Curso:** Big Data para Negocios  
**Instituicao:** UFC / MPCE  
**Professor Responsavel:** Luiz Alexandre Moreira Barros  
**Aluno(s):** Bruno Alves de Oliveira e Roberto  

---

## Visao Geral do Repositorio

Este repositorio centraliza todo o codigo-fonte, scripts, consultas SQL, relatorios em prosa e dashboards desenvolvidos ao longo do curso de **Big Data para Negocios**.

O conteudo esta organizado estritamente de acordo com a especificacao fornecida em `test/00_ESTRUTURA_REPOSITORIO.md`:

1. **Laboratorios (Labs 1 a 12)** — 30% da Nota Final.
2. **Avaliacao Final (Etapas 1 a 4)** — 70% da Nota Final (+ Bonus de Machine Learning).

---

## Estrutura de Pastas

```text
bigdata-curso-brunoroberto/
├── README.md                        <- Visao geral e instrucoes de execucao
├── COMO_VISUALIZAR_DASHBOARD.md     <- Guia rapido de acesso ao localhost do dashboard
├── servir_dashboard.py              <- Servidor HTTP local para abrir o dashboard em localhost
├── .gitignore                       <- Regras para exclusao de arquivos grandes/temporarios
│
├── dia1_fundamentos/
│   ├── lab01_hdfs/                  <- HDFS: Estrutura em camadas, replicacao 3x e simulacao
│   │   ├── comandos.sh
│   │   └── lab01_hdfs.py
│   └── lab02_sqoop/                 <- Ingestao relacional via Sqoop (MySQL / SQLite / DuckDB)
│       ├── import.sh
│       └── lab02_sqoop.py
│
├── dia2_transformacao/
│   ├── lab03_hive_tabelas/          <- Hive: Managed vs External tables (DROP table behavior)
│   │   ├── create_tables.sql
│   │   └── lab03_hive.py
│   ├── lab04_particoes/             <- Particionamento estatico e dinamico por ano/mes
│   │   ├── particionamento.sql
│   │   └── lab04_particoes.py
│   ├── lab05_bronze/                <- Camada Bronze: Limpeza e padronizacao dos dados brutos
│   │   ├── bronze.sql
│   │   └── lab05_bronze.py
│   ├── lab06_silver/                <- Camada Silver: Enriquecimento, juncoes e engenharia de atributos
│   │   ├── silver.sql
│   │   └── lab06_silver.py
│   ├── lab07_gold/                  <- Camada Gold: Tabelas agregadas orientadas a BI
│   │   ├── gold.sql
│   │   └── lab07_gold.py
│   └── lab08_eda/                   <- Analise Exploratoria de Dados (EDA queries)
│       ├── eda_queries.sql
│       └── lab08_eda.py
│
├── dia3_insights_bi/
│   ├── lab09_export/                <- Exportacao de dados para consumo em BI
│   │   ├── export.sh
│   │   └── lab09_export.py
│   ├── lab10_spark/                 <- Processamento distribuido com PySpark
│   │   └── spark_queries.py
│   ├── lab11_dashboard/             <- Geracao de Dashboard HTML interativo
│   │   ├── dashboard.py
│   │   └── dashboard_fraude.html
│   └── lab12_ml_preview/            <- Modelo preditivo de fraude (Preview ML)
│       └── modelo_fraude.py
│
└── avaliacao_final/
    ├── RELATORIO_AVALIACAO_FINAL.md <- Relatorio Consolidado Unificado (Etapas 1, 2, 3 e 4)
    ├── etapa1_arquitetura/          <- Desenho de Arquitetura de Big Data & Justificativa
    │   ├── diagrama.md
    │   └── justificativa.md
    ├── etapa2_bigdata/              <- Execucao de Pipeline Medallion em 30.000 transacoes
    │   ├── pipeline.py
    │   └── explicacao.md
    ├── etapa3_analise/              <- Analises de Negocio & Dashboard Executivo HTML
    │   ├── analises.py
    │   ├── generate_dashboard.py
    │   ├── servir_dashboard.py
    │   ├── dashboard.html
    │   └── ideia_bi.md
    └── etapa4_ml/                   <- Modelo Preditivo de Fraude com Regressao Logistica (Bonus)
        ├── modelo_fraude.py
        └── explicacao.md
```

---

## Compatibilidade de Ambientes (Rota A & Rota B)

O projeto suporta 100% das duas abordagens abordadas no curso:
- **Rota A (Cluster Real):** Hadoop HDFS + Apache Sqoop + Apache Hive + Apache Spark em cluster distribuido Linux.
- **Rota B (Sem Admin / Local):** Python 3 + DuckDB + PySpark Local + Plotly / HTML.

---

## Como Executar

### 1. Requisitos Locais (Rota B)
- Python 3.9+
- Dependencias Python: `pip install pandas duckdb plotly scikit-learn pyspark`

### 2. Acesso Rapido ao Dashboard em Localhost
Para abrir o Dashboard Executivo no seu navegador em `http://localhost:8000`:
```bash
python servir_dashboard.py
```
(Veja mais detalhes em `COMO_VISUALIZAR_DASHBOARD.md`).

### 3. Execucao dos Labs
- Cada diretorio de lab possui seus scripts `.sh` / `.sql` (para Rota A) e `.py` (para Rota B).
- Para executar qualquer lab localmente, navegue ate a pasta correspondente e rode o script Python:
  ```bash
  python dia1_fundamentos/lab01_hdfs/lab01_hdfs.py
  python dia2_transformacao/lab05_bronze/lab05_bronze.py
  python dia3_insights_bi/lab11_dashboard/dashboard.py
  ```

### 4. Execucao da Avaliacao Final
1. **Pipeline de Ingestao e Camadas (Etapa 2):**
   ```bash
   python avaliacao_final/etapa2_bigdata/pipeline.py
   ```
2. **Analises de Negocio e Dashboard (Etapa 3):**
   ```bash
   python avaliacao_final/etapa3_analise/analises.py
   ```
3. **Modelo Preditivo de Machine Learning (Etapa 4):**
   ```bash
   python avaliacao_final/etapa4_ml/modelo_fraude.py
   ```

---

## Documentacao da Avaliacao Final
Conforme a **Regra de Ouro** estabelecida na avaliacao, todos os relatorios presentes na pasta `avaliacao_final/` (`justificativa.md`, `explicacao.md`, `ideia_bi.md`) foram escritos rigorosamente em **prosa explicativa em portugues**, sem blocos de codigo colados, focando no raciocinio tecnico e no impacto de negocio.
