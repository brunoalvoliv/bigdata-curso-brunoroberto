# Etapa 3 — Descricao da Ideia e Estrategia do BI

## 1. Publico-Alvo do Dashboard

O **Painel Executivo de Prevencao a Fraude da TechPay** foi projetado para atender prioritariamente a dois publicos estrategicos dentro da empresa:

1. **Diretoria de Risco e Operacoes (nivel C-Level / VP):** Necessita de uma visao sintetizada e diaria sobre o apetite de risco da empresa, o impacto financeiro acumulado das perdas por fraude e a eficiencia das regras de bloqueio vigentes.
2. **Equipe de Analistas de Risco e Prevencao a Fraude (nivel Operacional):** Requer detalhamento tatico para identificar rapidamente anomalias em canais de captura especificos, surtos de fraude em categorias de estabelecimento comerciais e realizar *drill-down* sobre transacoes individuais marcadas com alto *risk score*.

---

## 2. Decisoes de Negocio Suportadas pelo Painel

O dashboard nao existe apenas para exibir dados estaticos, mas para direcionar acoes operacionais e de politica de credito. Ele orienta quatro decisoes cruciais na TechPay:

- **Ajuste Dinamico de Regras de Bloqueio por Canal:** Permite a equipe de risco identificar se o canal aplicativo (APP) esta sofrendo ataques coordenados e aplicar steps adicionais de autenticacao (como reconhecimento facial ou envio de biometria).
- **Gestao de Limites Noturnos (Politica de Madrugada):** Acompanha o pico de fraudes ocorrido entre 00h e 05h, justificando a imposicao automatica de teto de transferencia reduzido durante o periodo noturno para cartoes e contas de maior risco.
- **Restricao Contratual por Categoria de Estabelecimento:** Identifica categorias de maior sinistralidade (como o setor de viagens) e permite definir trava de seguranca para compras de valor elevado sem verificacao de dois fatores.
- **Revisao da Politica de Concessao de Limite por Segmento:** Permite avaliar o comportamento dos clientes classificados como *High-Risk*, ajustando os parametros de analise de credito inicial.

---

## 3. Racional de Escolha e Selecao dos KPIs

Os quatro indicadores primarios dispostos no topo do painel foram selecionados com base no impacto financeiro direto no P&L (Demonstracao do Resultado do Exercicio) da TechPay, tendo sido descartadas metricas secundarias de vaidade:

- **Total de Transacoes Processadas:** Oferece o denominador de volume operacional da plataforma.
- **Volume Financeiro Total (R$):** Indica a exposicao financeira total processada pela fintech.
- **Total de Transacoes Fraudulentas:** Revela a volumetria absoluta de ataques bem-sucedidos.
- **Taxa de Fraude (%) & Valor Total da Perda (R$):** E o KPI mestre da area de risco. Mede exatamente o percentual de contaminacao da operacao e a perda financeira liquida em reais. Metricas como quantidade de cliques ou tempo de navegacao no app foram descartadas por nao estarem correlacionadas diretamente a perda financeira por fraude.

---

## 4. Governanca, Frequencia de Leitura e Proprietario do Painel

- **Proprietario do Painel (Business Owner):** O Gerente Principal de Prevencao a Perdas e Prevencao a Fraude da TechPay.
- **Ritmo de Monitoramento e Leitura:**
  - **Acompanhamento Continuo (Diario):** Os analistas senior de risco monitoram o painel no inicio de cada jornada para identificar desvios da media movel.
  - **Reuniao Executiva Semanal:** A diretoria de risco utiliza o grafico de composicao e de tendencia horaria nas reunioes de comite de risco para deliberar sobre novas politicas de seguranca digital.

---

## 5. Relatorio de Achados de Negocio (Framework: Finding → Insight → Acao)

Para transformar as metricas da camada Gold em decisoes executivas concretas, as analises analiticas foram estruturadas segundo o framework **Finding (Constatacao) → Insight (Entendimento) → Acao (Intervencao de Negocio)**:

### Analise 1: Concentracao de Risco por Canal de Captura (`channel`)
- **Finding:** O canal **Aplicativo Mobile (APP)** apresentou uma taxa de fraude de 3,79%, superando em mais de 2 vezes a taxa observada nos canais ATM (1,80%), Web (1,74%) e POS (1,42%).
- **Insight:** Os fraudeadores priorizam o canal digital mobile devido à ausencia de friccao fisica (como insersao de cartao com chip ou biometria presencial) e à velocidade automatizada de execucao das transacoes.
- **Acao:** Implementar autenticacao biometrica facial obrigatoria e envio de token OTP via SMS/Push para todas as transacoes acima de R$ 500 originadas exclusivamente pelo aplicativo mobile.

### Analise 2: Sinistralidade por Categoria de Estabelecimento (`merchant_category`)
- **Finding:** A categoria de **Viagens e Passagens Aereas** registrou a maior taxa percentual de fraude (5,32%), mais do que o dobro da média observada nas demais categorias (como Alimentacao em 2,31%, Varejo em 2,24% e Eletronicos em 1,96%).
- **Insight:** Passagens aereas e produtos de viagens possuem altissima liquidez no mercado paralelo, permitindo que cartoes clonados ou roubados sejam rapidamente monetizados antes que o titular perceba a fraude e solicite o *chargeback*.
- **Acao:** Estabelecer uma regra de congelamento preventivo de 15 minutos para emissao de bilhetes aereos comprados por clientes de novo cadastro ou com score de risco superior a 60 pontos.

### Analise 3: Padrao Temporal e Janela Crítica da Madrugada em Compras de Viagem (`is_madrugada`)
- **Finding:** A combinacao do canal **APP** com a categoria **VIAGEM** no periodo da **MADRUGADA (True)** atingiu a taxa critica de fraude de **9,27%** (em comparacao a 7,58% fora da madrugada e menos de 2% no fluxo geral).
- **Insight:** A madrugada e o horario preferencial para ataques automatizados por robos (bots) e fraudes de sequestro/coacao, aproveitando-se do fato de que os clientes vitimas estao dormindo e demoram horas para notificar o banco.
- **Acao:** Impor um limite automatico de transferencia noturna de R$ 1.000 para todos os clientes Standard e High-Risk entre 00h e 06h no APP, exigindo confirmacao prévia realizada durante o dia para elevacao do teto.

### Analise 4: Vulnerabilidade por Segmento de Cliente (`segment`)
- **Finding:** O segmento enquadrado como **High-Risk** acumulou uma taxa de fraude de **9,67%**, em contraste drastico com os segmentos Standard (2,93%) e Premium (0,95%).
- **Insight:** A motorizacao de score de risco inicial da fintech identifica com precisao o perfil de fragilidade cadastral, porem as regras transacionais anteriores tratavam todos os segmentos com os mesmos limites de liquidez.
- **Acao:** Ajustar a matriz de apetite de risco para reduzir o limite de credito inicial de contas High-Risk e submete-las a verificacao de documentos adicional antes da liberacao de funcionalidades de transferencia instantanea.

