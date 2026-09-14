#!/usr/bin/env python3
"""
Lab 11: Dashboard de Fraudes (Plotly / HTML)
Curso: Big Data para Negócios
"""
import duckdb
import os
import plotly.express as px
import plotly.graph_objects as go

def main():
    print("=== Lab 11: Geração de Dashboard HTML Interativo ===")
    con = duckdb.connect()
    silver_path = "bigdata/silver/silver_transactions.parquet"
    out_html = "dia3_insights_bi/lab11_dashboard/dashboard_fraude.html"
    
    if not os.path.exists(silver_path):
        print(f"[ERRO] Arquivo {silver_path} não encontrado.")
        return
        
    # KPIs
    df_kpi = con.sql(f"""
    SELECT
        COUNT(*) AS total_tx,
        ROUND(SUM(amount), 2) AS vol_total,
        SUM(CASE WHEN is_fraud THEN 1 ELSE 0 END) AS total_fraudes,
        ROUND(SUM(CASE WHEN is_fraud THEN amount ELSE 0 END), 2) AS perda_fraude,
        ROUND(SUM(CASE WHEN is_fraud THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS taxa_fraude
    FROM '{silver_path}'
    """).df()

    kpi = df_kpi.iloc[0]

    # Gráfico 1: Fraude por Segmento
    df_seg = con.sql(f"""
    SELECT customer_segment, COUNT(*) AS tx, SUM(CASE WHEN is_fraud THEN 1 ELSE 0 END) AS fraudes
    FROM '{silver_path}' GROUP BY customer_segment
    """).df()
    fig1 = px.bar(df_seg, x='customer_segment', y=['tx', 'fraudes'], barmode='group', title="Transações vs Fraudes por Segmento")

    # Layout HTML Dashboard
    html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>TechPay - Executive Fraud Dashboard</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #0f172a; color: #f8fafc; margin: 0; padding: 20px; }}
        .header {{ display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #334155; padding-bottom: 15px; margin-bottom: 20px; }}
        .kpi-container {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin-bottom: 25px; }}
        .kpi-card {{ background: #1e293b; padding: 20px; border-radius: 10px; border: 1px solid #334155; text-align: center; }}
        .kpi-val {{ font-size: 28px; font-weight: bold; color: #38bdf8; margin-top: 5px; }}
        .kpi-title {{ font-size: 14px; color: #94a3b8; text-transform: uppercase; }}
        .chart-container {{ background: #1e293b; padding: 20px; border-radius: 10px; border: 1px solid #334155; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🛡️ TechPay — Painel Executivo de Prevenção a Fraudes</h1>
        <p>Monitoramento Diário de Risco</p>
    </div>
    <div class="kpi-container">
        <div class="kpi-card"><div class="kpi-title">Total Transações</div><div class="kpi-val">{int(kpi['total_tx']):,}</div></div>
        <div class="kpi-card"><div class="kpi-title">Volume Processado</div><div class="kpi-val">R$ {kpi['vol_total']:,.2f}</div></div>
        <div class="kpi-card"><div class="kpi-title">Total de Fraudes</div><div class="kpi-val" style="color:#ef4444">{int(kpi['total_fraudes']):,}</div></div>
        <div class="kpi-card"><div class="kpi-title">Perda Estimada em Fraude</div><div class="kpi-val" style="color:#ef4444">R$ {kpi['perda_fraude']:,.2f} ({kpi['taxa_fraude']}%)</div></div>
    </div>
    <div class="chart-container">
        {fig1.to_html(full_html=False, include_plotlyjs='cdn')}
    </div>
</body>
</html>
"""
    
    os.makedirs(os.path.dirname(out_html), exist_ok=True)
    with open(out_html, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    print(f"[OK] Dashboard HTML interativo gerado em '{out_html}'")

if __name__ == "__main__":
    main()
