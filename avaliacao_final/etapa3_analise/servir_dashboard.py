#!/usr/bin/env python3
"""
Servidor Local do Dashboard — TechPay (Etapa 3)
Executa um servidor HTTP local e abre o dashboard executivo no navegador.
"""
import http.server
import socketserver
import webbrowser
import os
import sys

PORT = 8000
DASHBOARD_FILE = "dashboard.html"

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    if not os.path.exists(DASHBOARD_FILE):
        print(f"[ERRO] Arquivo '{DASHBOARD_FILE}' nao encontrado no diretorio {script_dir}.")
        sys.exit(1)

    url = f"http://localhost:{PORT}/{DASHBOARD_FILE}"
    print("=================================================================")
    print("   SERVIDOR LOCAL DO DASHBOARD - TECHPAY (ETAPA 3)")
    print("=================================================================")
    print(f"Servidor HTTP rodando na porta {PORT}")
    print(f"Acesse diretamente em: {url}")
    print("Pressione Ctrl+C no terminal para encerrar.")
    print("=================================================================")

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
