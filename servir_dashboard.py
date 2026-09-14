#!/usr/bin/env python3
"""
Servidor Local do Dashboard — TechPay
Executa um servidor HTTP local e abre o dashboard executivo no navegador padrão.
"""
import http.server
import socketserver
import webbrowser
import os
import sys

PORT = 8000
DASHBOARD_PATH = "avaliacao_final/etapa3_analise/dashboard.html"

def main():
    if not os.path.exists(DASHBOARD_PATH):
        print(f"[ERRO] Arquivo '{DASHBOARD_PATH}' nao encontrado.")
        print("Execute o script a partir da raiz do repositorio.")
        sys.exit(1)

    url = f"http://localhost:{PORT}/{DASHBOARD_PATH}"
    print("=================================================================")
    print("   SERVIDOR LOCAL DO DASHBOARD - TECHPAY")
    print("=================================================================")
    print(f"Servidor HTTP rodando na porta {PORT}")
    print(f"Acesse diretamente em: {url}")
    print("Pressione Ctrl+C no terminal para encerrar.")
    print("=================================================================")

    # Abrir navegador automaticamente
    try:
        webbrowser.open(url)
    except Exception as e:
        print(f"[AVISO] Nao foi possivel abrir o navegador automaticamente: {e}")

    Handler = http.server.SimpleHTTPRequestHandler
    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor encerrado pelo usuario.")

if __name__ == "__main__":
    main()
