# Relatório Consolidado de Avaliação Final — Big Data para Negócios

**Curso:** Big Data para Negócios  
**Instituição:** Universidade Federal do Ceará (UFC) / Ministério Público do Estado do Ceará (MPCE)  
**Professor Responsável:** Luiz Alexandre Moreira Barros  
**Aluno(s):** Bruno Alves de Oliveira e Roberto  
**Cenário de Negócio:** Fintech TechPay — Análise de Risco, Arquitetura de Dados, Pipeline Medallion, Dashboard Executivo e Machine Learning  
**Link do Repositório:** `https://github.com/brunoalvoliv/bigdata-curso-brunoroberto.git`  

---

## Regra de Ouro da Entrega
Conforme estabelecido nas instruções da avaliação, este relatório foi redigido estritamente em **prosa explicativa em português**, sem blocos de código colados (`SELECT * FROM`, scripts Python ou comandos de shell). Todo o código-fonte executável encontra-se versionado e organizado nas pastas correspondentes dentro do repositório Git.

---

## Ambiente Técnico Utilizado
O projeto foi desenvolvido e executado utilizando a **Rota B (Sem Admin / Ambiente Local)**, empregando Python 3, DuckDB para execução de queries SQL otimizadas com formato Apache Parquet colunar, PySpark local para processamento distribuído simulado, Scikit-Learn para modelagem preditiva e Plotly / HTML5 para geração do dashboard interativo. A Rota B garante total equivalência conceitual à Rota A (Cluster Real Hadoop/Hive/Spark), oferecendo alta performance, portabilidade e reprodutibilidade imediata.

---

# Etapa 1 — Arquitetura de Big Data & Justificativa Técnica

## 1.1 Desenho do Fluxo de Dados (Arquitetura Medallion)
A arquitetura de dados projetada para a TechPay organiza o fluxo da informação desde os sistemas transacionais de origem até a tomada de decisão executiva, dividida em cinco camadas lógicas:

1. **Origem dos Dados (Sistemas Primários):** As transações financeiras originam-se em três canais operacionais da TechPay: o Aplicativo Mobile (via eventos JSON e APIs REST), a Aplicação Web (bancos relacionais PostgreSQL/MySQL) e os Caixas Eletrônicos (ATM) / Terminais POS (logs de terminal).
2. **Camada de Ingestão e Transporte:** Na modalidade em lote (batch), utiliza-se o Apache Sqoop (ou ingestores Python diretos via JDBC) para extração paralela dos bancos transacionais sem causar sobrecarga operacional nos servidores de produção.
3. **Camada Raw / Data Lake (Dados Brutos):** Armazenamento inicial dos arquivos em seu formato nativo (CSV/JSON), preservando o histórico bruto sem qualquer alteração de esquema para fins de auditoria e conformidade legal.
4. **Camada de Processamento Medallion (Apache Spark / DuckDB):**
   - **Bronze Layer (Sanitizada):** Conversão dos dados brutos para o formato colunar Apache Parquet com compressão Snappy, realizando sanitização de tipos, remoção de registros nulos críticos e eliminação de duplicações.
   - **Silver Layer (Enriquecida):** Aplicação de engenharia de atributos (derivação de hora do dia, flag de madrugada, faixas de valor e combinação de canais e estabelecimentos) e particionamento físico por `ano` e `mes`.
   - **Gold Layer (Agregados de BI):** Consolidação de tabelas analiticas agregadas por canal de captura, categoria de estabelecimento comercial, perfil temporal e segmento de cliente.
5. **Camada de Serving, BI & Machine Learning:** Disponibilização dos dados agregados para o Dashboard Executivo HTML5 interativo, alimentando simultaneamente o modelo preditivo de Machine Learning para cálculo de risco e alertas operacionais.

---

## 1.2 Justificativa Técnica das Decisões de Arquitetura

### 1. Escolha da Ferramenta de Ingestão e Alternativas Descartadas
A escolha do Apache Sqoop (ou conectores JDBC relacionais) fundamenta-se no fato de que as fontes primárias da TechPay consistem em bancos de dados relacionais SQL (PostgreSQL/MySQL). O Sqoop foi desenvolvido para realizar transferências em lote paralelas e eficientes entre sistemas relacionais e Data Lakes, aproveitando o paralelismo do ecossistema sem onerar o banco de produção.
- *Flume:* Descartado por ser voltado à coleta contínua de logs não estruturados, o que exigiria um trabalho adicional complexo de parsing para extrair dados financeiros estruturados.
- *Kafka:* Descartado para a ingestão batch primária devido à alta complexidade operacional (gerenciamento de clusters Zookeeper/KRaft, tópicos e esquemas Avro/JSON), sendo reservado exclusivamente para uma eventual expansão em streaming tempo real.

### 2. Estratégia de Particionamento e Cenário Real de Consulta
A camada Silver foi particionada fisicamente na estrutura de diretórios Hive por ano e mês (`ano/mes`). 
- *Justificativa de Consulta:* As equipes de risco e BI da TechPay investigam primordialmente padrões sazonais, comparativos mensais e fechamentos de fraude por período. Ao aplicar o filtro de data (ex.: `WHERE ano = 2025 AND mes = 8`), o motor analítico executa a técnica de **Partition Pruning** (Poda de Partições), ignorando a leitura de todo o restante do histórico. Isso reduz em mais de 90% a entrada e saída de disco (I/O) e acelera o tempo de resposta das consultas de minutos para milissegundos.

### 3. Pontos de Falha sob Crescimento de 100x e Mitigações
Com a expansão do volume da TechPay em 100 vezes (atingindo centenas de milhões de transações diárias), identificam-se três gargalos principais:
- **Gargalo no Banco Transacional:** Consultas batch do Sqoop simultâneas podem esgotar as conexões do banco de produção. *Mitigação:* Adotar réplicas de leitura (*read replicas*) dedicadas ou ingestão via Change Data Capture (CDC) com Debezium lendo os logs de transação (WAL/binlog).
- **Problema dos Arquivos Pequenos no NameNode:** Particionamento em granularidade muito fina (ex.: por hora) gera milhões de arquivos minúsculos que esgotam a memória RAM do NameNode do HDFS. *Mitigação:* Manter a granularidade mensal na Silver e rodar rotinas periódicas de compactação (*Small Files Compaction*), consolidando arquivos em blocos Parquet de 128 MB a 512 MB.
- **Ponto Único de Falha (SPOF):** Queda de instâncias únicas do NameNode ou do Metastore. *Mitigação:* Implementar alta disponibilidade (HA) com NameNodes ativo/standby sincronizados via Quorum Journal Manager (QJM).

### 4. Adaptação da Arquitetura para Detecção de Fraude em Tempo Real
Para bloquear fraudes em milissegundos antes da autorização da transação, a arquitetura passaria por quatro modificações centrais:
1. **Ingestão Continuada (Streaming):** Substituição do batch pelo Apache Kafka, publicando cada evento de transação no tópico `techpay.transactions.v1`.
2. **Processamento em Fluxo:** Uso de Spark Streaming ou Apache Flink para calcular agregações em janelas deslizantes (ex.: quantidade de tentativas do mesmo cartão nos últimos 5 minutos).
3. **Feature Store de Baixa Latência:** Armazenamento dos atributos calculados em bancos em memória de ultrabaixa latencia (Redis ou Cassandra).
4. **API de Predição:** Consulta ao modelo preditivo via API REST/gRPC durante o checkout, retornando a decisão de aprovação ou bloqueio em menos de 50 milissegundos.

---

# Etapa 2 — Execução do Pipeline de Big Data (Medallion)

## 2.1 Descrição das 6 Etapas do Pipeline
O pipeline sobre a base de 30.000 transações (`avaliacao_transactions.csv`) foi executado em seis etapas sequenciais:

1. **Ingestão Bruta:** Leitura do arquivo CSV original de 30.000 registros e gravação na pasta `raw/`, mantendo a fidelidade total dos campos.
2. **Criação da Tabela Raw:** Definição explícita do esquema das 12 colunas com seus respectivos tipos primitivos (inteiros, decimais, timestamps e strings).
3. **Particionamento:** Estruturação lógica e física dos dados com base nas colunas temporais extraídas (`ano` e `mes`).
4. **Camada Bronze (Sanitização e Limpeza):** Higienização dos dados, incluindo a conversão de textos para caixa baixa e remoção de espaços em branco (`TRIM/LOWER`), validação de valores monetários estritamente positivos (`amount > 0`), checagem de nulos em chaves primárias e conversão do campo de fraude para o tipo booleano nativo.
5. **Camada Silver (Enriquecimento de Atributos):** Derivação de colunas estratégicas de negócio: faixa de valor monetário (Baixo $<100$, Médio $100-1000$, Alto $>1000$), hora numérica do dia (0 a 23h), indicador booleano de período da madrugada (00h às 05:59h) e integração das dimensões de canal de captura (`channel`) e categoria de estabelecimento (`merchant_category`).
6. **Camada Gold (Agregações Orientadas a BI):** Consolidação de duas visões agregadas em Parquet: `gold_fraud_by_channel_category` (taxa e perda de fraude por cruzamento de canal e estabelecimento) e `gold_hourly_risk` (distribuição do risco por hora do dia e indicador de madrugada).

---

## 2.2 Volume e Rastreabilidade de Linhas
- **Linhas na Camada Raw:** 30.000 transações.
- **Linhas Sobreviventes na Bronze e Silver:** 30.000 transações (100% de aproveitamento).
- **Justificativa de Descarte:** Nenhuma linha precisou ser eliminada, pois todas as 30.000 transações continham identificadores válidos de cliente e transação, além de valores monetários positivos, garantindo integridade e auditabilidade completa dos dados.

---

## 2.3 Justificativa do Uso das Colunas `channel` e `merchant_category`
Em operações reais de meios de pagamento, a fraude não ocorre de maneira uniforme apenas com base no perfil do cliente; ela está fortemente associada ao **mecanismo de captura** e ao **tipo de bem transacionado**.
- **Canal de Captura (`channel`):** Golpistas preferem canais digitais sem presença física (aplicativos móveis e web e-commerce) em detrimento de caixas eletrônicos (ATM) ou maquininhas presenciais (POS).
- **Categoria do Estabelecimento (`merchant_category`):** Fraudes concentram-se em categorias de alta liquidez e rápida conversão em dinheiro no mercado ilegal, como passagens aéreas/viagens e eletrônicos.
- A inclusão dessas duas colunas na camada Silver permitiu cruzar o canal com o estabelecimento, revelando as combinações exatas de maior vulnerabilidade da empresa.

---

## 2.4 Estrutura e Propósito das Agregações da Camada Gold
- **`gold_fraud_by_channel_category`:** Agrupa o volume total de transações, o volume financeiro processado, o número absoluto de fraudes, o valor total perdido em reais e a taxa percentual de fraude por combinação de canal e categoria. Responde diretamente quais produtos digitais demandam etapas adicionais de autenticação (2FA/Biometria).
- **`gold_hourly_risk`:** Agrupa a taxa de fraude por hora do dia e destaca a janela noturna da madrugada. Fundamenta a decisão operacional de definir limites de transferência noturna diferenciados.

---

# Etapa 3 — Análise de Negócio & Dashboard Executivo

## 3.1 Relatório de Achados de Negócio (Framework: Finding → Insight → Ação)

### Análise 1: Concentração de Risco por Canal de Captura (`channel`)
- **Finding (Constatação):** O canal **Aplicativo Mobile (APP)** apresentou a maior taxa de fraude da empresa, atingindo **3,79%** (455 fraudes em 12.021 transações), superando em mais de duas vezes as taxas observadas nos canais ATM (1,80%), Web (1,74%) e POS (1,42%).
- **Insight (Entendimento):** Criminosos exploram a conveniência do app móvel devido ao alto volume de transações e à facilidade de automação por scripts, aproveitando-se de cadastros frágeis sem validação presencial.
- **Ação (Intervenção):** Tornar obrigatória a validação de biometria facial no app para todas as transações acima de R$ 500 ou originadas de novos dispositivos.

### Análise 2: Sinistralidade por Categoria de Estabelecimento (`merchant_category`)
- **Finding (Constatação):** A categoria de **Viagens e Passagens Aéreas** registrou a taxa de fraude mais alta entre todos os segmentos, alcançando **5,32%** (160 fraudes em 3.010 transações), enquanto categorias como Alimentação (2,31%), Varejo (2,24%) e Eletrônicos (1,96%) mantiveram médias muito inferiores.
- **Insight (Entendimento):** Bilhetes aéreos e pacotes de viagem possuem altíssimo valor de revenda imediata no mercado paralelo, permitindo que o fraudador monetize o golpe antes do cancelamento do cartão pelo titular.
- **Ação (Intervenção):** Aplicar uma trava de segurança com retenção preventiva de 15 minutos para emissão de passagens aéreas compradas por usuários com score de risco elevado.

### Análise 3: Padrão Temporal e Combinação Crítica na Madrugada (`is_madrugada`)
- **Finding (Constatação):** A combinação do canal **APP** com a categoria **VIAGEM** durante o período da **MADRUGADA (00h às 05:59h)** atingiu a taxa crítica de fraude de **9,27%** (29 fraudes em 313 transações), contra 7,58% fora da madrugada e menos de 2% na média geral diurna.
- **Insight (Entendimento):** A janela noturna é o momento de maior vulnerabilidade, combinando ataques automatizados por robôs noturnos com a impossibilidade de contato telefônico imediato com a vítima para confirmação.
- **Ação (Intervenção):** Impor um limite rígido de transferência noturna de R$ 1.000 entre 00h e 06h no aplicativo para contas dos segmentos Standard e High-Risk.

### Análise 4: Vulnerabilidade por Segmento de Cliente (`segment`)
- **Finding (Constatação):** Clientes classificados no segmento **High-Risk** apresentaram uma taxa de fraude de **9,67%** (282 fraudes em 2.915 transações), em contraste marcante com o segmento Standard (2,93%) e o segmento Premium (**0,95%**).
- **Insight (Entendimento):** O motor de score cadastral da TechPay consegue segmentar com precisão os perfis de risco na abertura da conta, mas a operação não aplicava travas diferenciadas de limite por segmento.
- **Ação (Intervenção):** Reduzir em 50% o limite de concessão inicial para novas contas classificadas como High-Risk e exigir comprovação documental complementar.

---

## 3.2 Estrutura e Funcionalidade do Dashboard Executivo
O dashboard interativo em HTML5 ([dashboard.html](file:///d:/GitHub/mba_ufc/bigdata-curso-brunoroberto/avaliacao_final/etapa3_analise/dashboard.html)) foi construído com Plotly.js e CSS dark-mode, dividido em quatro blocos visuais:

1. **Bloco de KPIs (Topo):** Exibe 4 cards estratégicos: Total de Transações (30.000), Volume Financero Processado (R\$ 15.340.231,10), Total de Transações Fraudulentas (751) e Taxa de Fraude % / Perda Financeira Acumulada (2,50% / R\$ 382.410,50).
2. **Bloco de Tendência Horária (Esquerda):** Gráfico de linha interativo destacando a variação da taxa percentual de fraude ao longo das 24 horas do dia, evidenciando o pico no período da madrugada.
3. **Bloco de Composição do Risco (Direita):** Gráfico de barras agrupadas comparando a taxa de fraude por categoria de estabelecimento nos quatro canais de captura.
4. **Bloco de Detalhamento Operacional (Base):** Tabela interativa com as 10 transações de maior *risk score*, permitindo aos analistas realizar auditabilidade rápida sobre transações suspeitas de alto valor.

---

## 3.3 Descrição da Ideia do BI como Produto
- **Público-Alvo:** Diretoria de Risco/Operações (visão executiva consolidada) e Analistas de Prevenção à Fraude (investigação tática e operacional).
- **Decisões Orientadas:** Ajuste de regras de bloqueio por canal, gestão de limites noturnos, restrição por categoria comercial e revisão de concedimento de crédito por segmento.
- **Racional de KPIs:** Foco exclusivo nas métricas que impactam a perda financeira direta no resultado da empresa (Volume, Taxa de Contaminação e Perda em Reais), descartando métricas de vaidade sem correlação com risco.
- **Proprietário do Painel:** Gerente Principal de Prevenção a Perdas da TechPay, com acompanhamento diário pelos analistas e revisão semanal pelo comitê executivo de risco.

---

# Etapa 4 — Modelo Preditivo de Fraude (Machine Learning)

## 4.1 Escolha do Algoritmo e Preparação dos Dados
Para a modelagem preditiva de fraude (desenvolvida em `modelo_fraude.py`), adotou-se o algoritmo de **Regressão Logística** com ajuste de pesos balanceados (`class_weight='balanced'`).
- **Justificativa do Algoritmo:** A Regressão Logística é o padrão da indústria financeira por oferecer alta capacidade discriminatória associada à total interpretabilidade dos coeficientes (ao contrário de modelos caixas-pretas), permitindo fundamentar regras de bloqueio perante órgãos reguladores.
- **Tratamento de Desbalanceamento e Padronização:** Como a fraude representa 2,5% dos eventos na base, aplicou-se o `StandardScaler` para normalizar as variáveis numéricas (`amount`, `credit_score`, `risk_score`) e ponderou-se a função de perda para penalizar severamente os erros de falsos negativos.

---

## 4.2 Desempenho Global e Métricas do Modelo
O modelo foi treinado em 70% da base e avaliado em um conjunto de teste independente contendo 9.000 transações:
- **ROC-AUC Score:** **0.7292**, demonstrando forte capacidade de ordenação e separação de risco.
- **Sensibilidade / Recall em Fraudes:** **56%** (capturou 131 das 225 fraudes presentes no lote de teste antes da liquidação).
- **Acurácia Global:** **76%** (mantendo um equilíbrio entre contenção de perdas e retenção aceitável de alarmes falsos para revisão).

---

## 4.3 Interpretação dos Coeficientes e Recomendações
Os coeficientes estimados pelo modelo revelaram a importância relativa de cada variável para o aumento da probabilidade de fraude:

1. **Segmento High-Risk (`is_seg_highrisk` - Peso: +0.5691):** É o principal fator individual de risco na plataforma.
2. **Canal APP (`is_channel_app` - Peso: +0.4827):** Segundo maior preditor positivo de fraude.
3. **Categoria Viagem (`is_cat_viagem` - Peso: +0.2834):** Terceiro maior peso positivo.
4. **Horório de Madrugada (`is_madrugada` - Peso: +0.1589):** Confirma o impacto do período noturno na probabilidade de fraude.

### Recomendações de Ação:
- **Regra de Bloqueio Automático:** Configurar o motor de risco para exigir verificação biométrica em duas etapas (2FA) sempre que a transação combinar canal **APP**, categoria **VIAGEM** e horário de **MADRUGADA**.
- **Score Dinâmico no Checkout:** Integrar a probabilidade do modelo ao gateway de pagamentos para declinar automaticamente compras com score de probabilidade superior a 80%.

---

# Conclusão e Resumo de Arquivos do Repositório

Todos os artefatos da avaliação final estão devidamente commitados e organizados na pasta `avaliacao_final/` no repositório Git:

- **Etapa 1 (Arquitetura):** [`avaliacao_final/etapa1_arquitetura/diagrama.md`](file:///d:/GitHub/mba_ufc/bigdata-curso-brunoroberto/avaliacao_final/etapa1_arquitetura/diagrama.md) e [`justificativa.md`](file:///d:/GitHub/mba_ufc/bigdata-curso-brunoroberto/avaliacao_final/etapa1_arquitetura/justificativa.md)
- **Etapa 2 (Pipeline Medallion):** [`avaliacao_final/etapa2_bigdata/pipeline.py`](file:///d:/GitHub/mba_ufc/bigdata-curso-brunoroberto/avaliacao_final/etapa2_bigdata/pipeline.py) e [`explicacao.md`](file:///d:/GitHub/mba_ufc/bigdata-curso-brunoroberto/avaliacao_final/etapa2_bigdata/explicacao.md)
- **Etapa 3 (Análise & BI):** [`avaliacao_final/etapa3_analise/analises.py`](file:///d:/GitHub/mba_ufc/bigdata-curso-brunoroberto/avaliacao_final/etapa3_analise/analises.py), [`generate_dashboard.py`](file:///d:/GitHub/mba_ufc/bigdata-curso-brunoroberto/avaliacao_final/etapa3_analise/generate_dashboard.py), [`dashboard.html`](file:///d:/GitHub/mba_ufc/bigdata-curso-brunoroberto/avaliacao_final/etapa3_analise/dashboard.html) e [`ideia_bi.md`](file:///d:/GitHub/mba_ufc/bigdata-curso-brunoroberto/avaliacao_final/etapa3_analise/ideia_bi.md)
- **Etapa 4 (Machine Learning):** [`avaliacao_final/etapa4_ml/modelo_fraude.py`](file:///d:/GitHub/mba_ufc/bigdata-curso-brunoroberto/avaliacao_final/etapa4_ml/modelo_fraude.py) e [`explicacao.md`](file:///d:/GitHub/mba_ufc/bigdata-curso-brunoroberto/avaliacao_final/etapa4_ml/explicacao.md)
- **Instruções de Visualização do Dashboard:** [`COMO_VISUALIZAR_DASHBOARD.md`](file:///d:/GitHub/mba_ufc/bigdata-curso-brunoroberto/COMO_VISUALIZAR_DASHBOARD.md)
