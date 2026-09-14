# Justificativa da Arquitetura de Big Data — TechPay

## 1. Escolha da Ferramenta de Ingestao e Alternativas Descartadas

Para o pipeline atual da TechPay, a escolha principal de ferramenta de ingestao batch recai sobre o Apache Sqoop (ou ingestores equivalentes baseados em conexao direta JDBC/SQL). Esta escolha justifica-se pelo fato de que as fontes de dados primarias da empresa consistem em bancos de dados relacionais transacionais (como PostgreSQL e MySQL) que registram historico de transacoes financeiras e dados cadastrais de clientes. O Apache Sqoop foi projetado especificamente para realizar a transferencia em lote eficiente entre bancos relacionais e sistemas de armazenamento distribuido como o HDFS, utilizando tarefas paralelas do MapReduce sem sobrecarregar o banco de dados de origem.

Alternativas como o Apache Flume e o Apache Kafka foram analisadas e descartadas para a ingestao batch primaria nesta fase. O Flume e orientado prioritariamente para a coleta de arquivos de log nao estruturados em fluxo continuo, o que demandaria parsing adicional para estruturar os registros financeiros. O Apache Kafka, embora seja a ferramenta padrao para mensageria de alta performance, introduziria uma complexidade operacional excessiva (necessidade de cluster Zookeeper/KRaft, gerenciamento de topicos e retencao) se o objetivo imediato for a carga diaria ou horaria em lote a partir do banco transacional. O Sqoop proporciona uma solucao direta, nativa do ecossistema Hadoop, com conversao automatica de schemas e extracao paralela otimizada por chave primaria.

---

## 2. Estrategia de Particionamento e Justificativa de Consulta

A estrategia de particionamento adotada nas camadas intermediaria (Silver) e analitica (Gold) baseia-se na chave composta de tempo: **ano** e **mes** (`ano` / `mes`). 

A justificativa tecnica fundamenta-se nos padroes de consulta mais frequentes das equipes de Risco, Fraude e BI da TechPay. Consultas analiticas de prevencao a fraude e fechamento financeiro raramente buscam transacoes individuais de forma isolada sem filtro temporal; pelo contrario, analistas investigam tendencias mensais, comparativos ano a ano e variacoes sazonais de comportamento do consumidor (como Black Friday e festividades).

Ao particionar os dados fisicamente em diretorios por ano e mes dentro do armazenamento em formato Apache Parquet, o mecanismo de execucao de consultas (seja Apache Hive, Spark SQL ou DuckDB) aplica a tecnica de **Partition Pruning** (Poda de Particoes). Isso significa que, ao executar uma consulta focada no ultimo trimestre, o motor analitico ignora completamente a leitura de anos e meses nao solicitados. Em um ambiente com bilhoes de linhas, essa estrategia reduz a E/S de disco em mais de 90%, acelera a velocidade de resposta das queries de horas para segundos e otimiza o consumo de memoria do cluster.

---

## 3. Pontos de Falha da Arquitetura e Mitigacao sob Crescimento de 100x

Em um cenario de expansao em que o volume de dados da TechPay multiplique por 100 (passando de dezenas de milhares para centenas de milhoes de transacoes diarias), os principais pontos de falha identificados no desenho atual seriam:

1. **Gargalo no Banco Transacional de Origem durante a Ingestao Batch:** Conexoes JDBC paralelas massivas do Sqoop podem esgotar as conexoes do banco relacional de producao, causando degradacao do aplicativo TechPay.
   - *Mitigacao:* Implementar a leitura a partir de replicas de leitura (*read replicas*) dedicadas ou adotar ingestao por Change Data Capture (CDC) via Debezium, lendo os logs de transacao do banco (WAL/binlog) sem impacto no banco principal.
2. **Gargalo de Memoria no NameNode do HDFS (Problema dos Arquivos Pequenos):** Se o particionamento for mal dimensionado (ex.: particionar por dia ou por hora), milhoes de arquivos pequenos serao gerados, sobrecarregando a memoria RAM do NameNode.
   - *Mitigacao:* Manter a granularidade de particionamento em nivel mensal na camada Silver e aplicar rotinas de compactacao periodica (*small files compaction*) que consolidam arquivos menores em blocos Parquet ideais de 128 MB a 512 MB.
3. **Ponto Unico de Falha nos Daemons Principais:** Dependencia de instancias unicas do NameNode ou do Metastore.
   - *Mitigacao:* Configurar HDFS High Availability (HA) com NameNodes ativo e standby sincronizados via Quorum Journal Manager (QJM).

---

## 4. Adequacao da Arquitetura para Deteccao de Fraude em Tempo Real

Se a diretoria da TechPay demandasse **deteccao e bloqueio de fraude em tempo real** (com tomada de decisao em milissegundos antes da aprovacao da transacao), o fluxo de dados precisaria passar por uma transformacao arquitetural profunda:

1. **Camada de Ingestao em Fluxo (Streaming Ingestion):** O modelo batch via Sqoop seria substituido por uma arquitetura orientada a eventos usando **Apache Kafka**. Cada transacao realizada no aplicativo ou terminal POS seria publicada imediatamente em um topico Kafka (`techpay.transactions.v1`).
2. **Camada de Processamento Continuo (Stream Processing):** Em vez de jobs agendados de hora em hora no Hive/Spark, utilizaria-se **Spark Streaming** ou **Apache Flink**. O motor de streaming processaria as transacoes janela a janela (ex.: janelas deslizantes de 5 minutos) para calcular agregacoes em tempo real, como contagem de transacoes recentes do mesmo cartao em cidades distintas.
3. **Inclusao de uma Feature Store e Banco de Baixa Latencia:** As variaveis calculadas seriam mantidas em um armazenamento em memoria de ultrabaixa latencia (como Redis ou Apache Cassandra). O modelo preditivo de Machine Learning seria consultado via API REST / gRPC em tempo de execucao da transacao, retornando o *score* de risco e a decisao (aprovar ou negar) em menos de 50 milissegundos.
4. **Camada Medallion como Repositorio Historico:** O ambiente Medallion no Data Lake continuaria existindo via mensageria (Kafka Connect salvando no HDFS/S3), assumindo a responsabilidade de treinamento assincrono dos modelos preditivos e relatorios executivos de BI.
