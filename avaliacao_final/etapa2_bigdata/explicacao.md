# Etapa 2 — Relatorio Explicativo do Pipeline de Big Data

## 1. Descricao das Etapas Executadas no Pipeline

A implementacao do pipeline de dados da TechPay foi construida seguindo rigorosamente o padrao de Arquitetura Medallion, dividida em seis etapas sequenciais de ingestao, sanitizacao, enriquecimento e agregacao:

1. **Ingestao dos Dados Brutos:** A base contendo 30.000 registros transacionais foi lida a partir do arquivo original e depositada no repositorio bruto da camada Raw. Nesta etapa, nenhuma transformacao de schema foi aplicada, mantendo a integridade dos tipos em texto e os nomes de colunas conforme fornecidos na origem.
2. **Criacao da Tabela Raw com Tipagem Controlada:** Foi mapeado o esquema inicial declarando os tipos primarios para as 12 colunas da base (identificadores inteiros, valores decimais, carimbos de data/hora e variaveis categoricas).
3. **Estrategia de Particionamento:** Os registros foram estruturados com suporte a particionamento temporal dinamico por ano e mes, extraidos a partir da coluna de carimbo de data/hora, otimizando futuras varreduras de consulta.
4. **Processamento da Camada Bronze (Sanitizacao e Limpeza):** Aplicou-se a padronizacao de campos de texto (conversao para minusculas e remocao de espacos em branco), tratamento de valores nulos ou ausentes, validacao de valores monetarios estritamente positivos e mapeamento explicito do campo de fraude para tipo booleano.
5. **Processamento da Camada Silver (Enriquecimento de Atributos):** Os dados limpos foram enriquecidos atraves da engenharia de atributos. Foram derivadas colunas estrategicas como o horario numerico do dia (0 a 23 horas), a marcacao booleana para transacoes ocorridas no periodo da madrugada (entre 00:00 e 05:59), a categorizacao em faixas de valor (Baixo, Medio e Alto) e o agrupamento combinado das novas dimensoes de canal e categoria de estabelecimento.
6. **Processamento da Camada Gold (Visoes Agregadas de BI):** Foram consolidadas duas tabelas analiticas otimizadas para consumo de BI: a primeira agregando a taxa e o volume financeiro de fraude pela combinacao de canal transacional e categoria de estabelecimento; a segunda analisando o comportamento do risco por hora do dia e indicador de madrugada.

---

## 2. Metricas de Volume e Linhas Sobreviventes

Da carga inicial contendo 30.000 registros brutos na camada Raw, todas as 30.000 linhas atenderam aos criterios de integridade estrita (existencia de identificador de transacao valido, cliente associado e valor monetario positivo), sendo 100% integradas às camadas Bronze e Silver. Nenhuma linha precisou ser descartada por inconsistencia de formato, garantindo total rastreabilidade auditavel dos dados da TechPay.

---

## 3. Justificativa Tecnica do Uso das Colunas `channel` e `merchant_category`

A decisao de incluir ativamente as novas colunas `channel` (aplicativo, web, POS e caixa eletronico) e `merchant_category` (varejo, viagem, eletronicos, alimentacao, servicos e saude) na camada Silver fundamenta-se na natureza real dos padroes de fraude financeira.

Diferente do comportamento simplificado observado em analises genericas em que a fraude se concentra apenas no segmento do cliente, em operacoes reais de pagamento a fraude esta altamente correlacionada ao canal de captura e ao tipo de estabelecimento. Golpistas utilizam prioritariamente canais digitais de baixa friccao fisica (como aplicativos moveis e e-commerce) e focam a compra em bens de alta liquidez ou servicos com baixo prazo de cancelamento (como bilhetes de viagem e eletronicos). 

Ao incorporar essas duas colunas na camada Silver, o pipeline permitiu cruzar o canal de transacao com a categoria do estabelecimento comercial, viabilizando a identificacao da combinacao exata de maior risco na empresa, algo impossivel de detectar sem essas dimensoes.

---

## 4. Estrutura e Proposito das Agregacoes da Camada Gold

As duas tabelas agregadas geradas na camada Gold foram desenhadas especificamente para responder às tres necessidades prioritarias da diretoria de risco da TechPay:

- **Tabela Gold de Canal e Categoria (`gold_fraud_by_channel_category`):** Agrupa o volume total processado, o numero de transacoes confirmadas como fraude, o valor financeiro perdido e a taxa percentual de fraude por cruzamento de canal e segmento de estabelecimento. Esta tabela responde diretamente qual combinacao de produto digital exige regras de autenticacao reforcada (como biometria facial ou OTP).
- **Tabela Gold de Distribuição Temporal (`gold_hourly_risk`):** Agrupa a taxa de fraude por hora do dia e destaca a janela da madrugada. Esta tabela subsidia a equipe de operacoes no ajuste de limites automaticos de transferencia noturna, reduzindo drasticamente o risco sem impactar transacoes legitimas em horario comercial.
