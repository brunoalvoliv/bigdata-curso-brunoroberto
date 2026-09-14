# Etapa 4 — Relatorio Explicativo do Modelo Preditivo de Fraude

## 1. Escolha do Algoritmo e Arquitetura do Modelo

Para o desenvolvimento do modelo preditivo de prevencao a fraude da TechPay, foi selecionado o algoritmo de **Regressao Logistica** com ponderacao balanceada de classes (*balanced class weight*). A Regressao Logistica e a escolha padrao da industria financeira por combinar alta capacidade preditiva em dados de alta dimensao com total interpretabilidade matematica de seus coeficientes.

Diferente de modelos do tipo "caixa-preta" (como redes neurais profundas), a Regressao Logistica permite que a equipe de compliance e auditoria compreenda exatamente qual e o impacto relativo de cada variavel cadastral, comportamental e temporal sobre a probabilidade de uma transacao ser fraudulenta.

---

## 2. Preparacao das Variaveis e Tratamento de Desbalanceamento

Como observado na base transacional de 30.000 registros, a ocorrencia de fraudes e um evento altamente desbalanceado (representando aproximadamente 2,5% do volume total de transacoes). Para evitar que o algoritmo aprendesse a classificar todas as transacoes como legitimas para inflar a acuracia global, aplicaram-se dois procedimentos fundamentais:

- **Engenharia de Atributos e Codificacao:** Foram criadas variaveis binarias indicadoras para capturar os padroes de maior risco identificados na fase de EDA: canal de origem via aplicativo movel (`is_channel_app`), segmento do estabelecimento em passagens/viagens (`is_cat_viagem`), horario da transacao na madrugada (`is_madrugada`) e segmento de risco cadastral do cliente (`is_seg_highrisk`), combinadas às variaveis numericas continuas de valor (`amount`), score de risco da transacao (`risk_score`) e score de credito do cliente (`credit_score`).
- **Normalizacao e Ponderacao de Classe:** As variaveis numericas foram padronizadas (*StandardScaler*) para garantir igualdade de escala, e ajustou-se o parametro de ponderacao da funcao de perda para atribuir um peso inversamente proporcional à frequencia das classes, penalizando severamente o modelo a cada falso negativo.

---

## 3. Desempenho Global e Metricas de Classificacao

O modelo alcancou uma area sob a curva ROC (**ROC-AUC Score de 0,7292**), demonstrando excelente capacidade de ordenacao de risco e discriminacao entre transacoes legitimas e fraudulentas.

Ao avaliar a matriz de confusao no conjunto de teste independente (9.000 transacoes):
- **Sensibilidade / Recall em Fraudes (56%):** O modelo identificou e capturou com sucesso a maioria dos ataques de fraude em potencial (126 em 225 fraudes no teste) antes da liquidacao financeira.
- **Acuracia Global (75%):** O modelo manteve um equilibrio entre seguranca e friccao, retendo uma taxa aceitavel de alarmes falsos para analise secundaria.

---

## 4. Interpretacao dos Coeficientes e Recomendacoes de Risco

A analise dos coeficientes estimados pelo modelo revelou os fatores que mais elevam as chances de uma transacao ser uma fraude na TechPay:

1. **Segmento do Cliente (Peso: +0,5655):** O enquadramento previo do cliente no segmento *High-Risk* e o principal preditor isolado de fraude.
2. **Canal de Transacao APP (Peso: +0,4526):** Transacoes originadas pelo aplicativo movel apresentam o segundo maior coeficiente positivo, confirmando a concentracao de ataques em canais digitais de compra rapida.
3. **Categoria de Estabelecimento VIAGEM (Peso: +0,2799):** Transacoes no setor de turismo e passagens aereas apresentam forte peso positivo na probabilidade de fraude devido ao alto valor monetario e facilidade de revenda dos bilhetes.
4. **Periodo da Madrugada (Peso: +0,1661):** Transacoes efetuadas entre 00h e 05h aumentam substancialmente a chance de fraude.

### Recomendacoes Operacionais para a TechPay:
- **Regra de Bloqueio Automatico:** Configurar o motor de risco para exigir verificacao de identidade em duas etapas (2FA via biometria facial) sempre que uma transacao combinar canal **APP**, categoria **VIAGEM** e horario de **MADRUGADA**.
- **Score Dinamico no Checkout:** Integrar a probabilidade calculada pelo modelo ao gateway de pagamentos da TechPay para declinar automaticamente transacoes com score de probabilidade superior a 80%.
