# Como Visualizar o Dashboard Executivo no Localhost

Para facilitar a avaliacao e permitir a visualizacao interativa do **Dashboard Executivo de Prevencao a Fraudes (TechPay)** diretamente no seu navegador em `http://localhost:8000`, disponibilizamos duas formas simples de execucao:

---

## Opcao 1: Execucao Rapida com Script Python (Recomendado)

Rode o comando abaixo a partir do terminal na raiz do repositorio:

```bash
python servir_dashboard.py
```

Ou a partir da pasta da Etapa 3:

```bash
python avaliacao_final/etapa3_analise/servir_dashboard.py
```

### O que o script faz:
1. Inicia um servidor HTTP local na porta 8000.
2. Abre automaticamente o seu navegador padrao no endereco `http://localhost:8000/avaliacao_final/etapa3_analise/dashboard.html`.
3. Para encerrar o servidor a qualquer momento, basta pressionar `Ctrl+C` no terminal.

---

## Opcao 2: Execucao Manual com Servidor HTTP Nativo do Python

Se preferir rodar manualmente sem utilizar o script auxiliar:

1. Inicie o servidor HTTP do Python na raiz do projeto:
   ```bash
   python -m http.server 8000
   ```

2. Abra o seu navegador e acesse a URL:
   [http://localhost:8000/avaliacao_final/etapa3_analise/dashboard.html](http://localhost:8000/avaliacao_final/etapa3_analise/dashboard.html)

---

## Opcao 3: Abertura Direta do Arquivo HTML

Caso nao queira rodar um servidor HTTP, voce tambem pode abrir o arquivo estatico diretamente no navegador dando um duplo clique no arquivo:
`avaliacao_final/etapa3_analise/dashboard.html`

*Nota: O dashboard contem todos os graficos Plotly.js e folhas de estilo CSS embutidos de forma autonoma.*
