#!/usr/bin/env python3
"""
Gera o Dashboard Executivo HTML Interativo para a Etapa 3 da Avaliação Final
"""
import duckdb
import os
import plotly.express as px
import plotly.graph_objects as go

def main():
    con = duckdb.connect()
    silver_path = "avaliacao_final/etapa2_bigdata/data/silver/silver_transactions.parquet"
    out_html = "avaliacao_final/etapa3_analise/dashboard.html"
    
    # 1. KPIs Principais
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
    
    # 2. Bloco de Tendência: Distribuição de Fraudes por Hora do Dia (00h a 23h)
    df_hourly = con.sql(f"""
    SELECT hora_dia, COUNT(*) AS total_tx, SUM(CASE WHEN is_fraud THEN 1 ELSE 0 END) AS fraudes,
           ROUND(SUM(CASE WHEN is_fraud THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS taxa_fraude_pct
    FROM '{silver_path}' GROUP BY hora_dia ORDER BY hora_dia
    """).df()
    
    fig_trend = px.line(df_hourly, x='hora_dia', y='taxa_fraude_pct', markers=True,
                        title="<b>Tendência Horária: Taxa de Fraude % por Hora do Dia</b>",
                        labels={'hora_dia': 'Hora do Dia (0h-23h)', 'taxa_fraude_pct': 'Taxa de Fraude (%)'})
    fig_trend.update_traces(line_color='#ef4444', line_width=3)
    fig_trend.update_layout(template='plotly_dark', paper_bgcolor='#1e293b', plot_bgcolor='#0f172a')
    
    # 3. Bloco de Composição: Matriz de Fraude por Canal vs Categoria de Estabelecimento
    df_comp = con.sql(f"""
    SELECT channel, merchant_category, ROUND(SUM(CASE WHEN is_fraud THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS taxa_fraude_pct
    FROM '{silver_path}' GROUP BY channel, merchant_category
    """).df()
    fig_comp = px.bar(df_comp, x='merchant_category', y='taxa_fraude_pct', color='channel', barmode='group',
                      title="<b>Composição do Risco: Taxa de Fraude por Canal e Categoria</b>",
                      labels={'merchant_category': 'Categoria de Estabelecimento', 'taxa_fraude_pct': 'Taxa de Fraude (%)'})
    fig_comp.update_layout(template='plotly_dark', paper_bgcolor='#1e293b', plot_bgcolor='#0f172a')

    # 4. Tabela de Detalhe: Top 10 Transações de Maior Risco de Fraude
    df_detail = con.sql(f"""
    SELECT transaction_id, customer_id, segment, channel, merchant_category, amount, risk_score, status
    FROM '{silver_path}'
    WHERE is_fraud = TRUE
    ORDER BY risk_score DESC, amount DESC
    LIMIT 10
    """).df()
    
    table_rows = ""
    for _, r in df_detail.iterrows():
        table_rows += f"""<tr>
            <td>#{int(r['transaction_id'])}</td>
            <td>Cliente #{int(r['customer_id'])}</td>
            <td><span class="badge {r['segment'].lower()}">{r['segment']}</span></td>
            <td>{r['channel'].upper()}</td>
            <td>{r['merchant_category'].capitalize()}</td>
            <td>R$ {r['amount']:,.2f}</td>
            <td style="color:#ef4444; font-weight:bold;">{r['risk_score']:.1f}</td>
            <td><span class="badge status-{r['status']}">{r['status']}</span></td>
        </tr>"""

    # HTML Final
    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>TechPay - Risk & Fraud Analytics Dashboard</title>
    <style>
        body {{ font-family: 'Inter', system-ui, -apple-system, sans-serif; background-color: #0f172a; color: #f8fafc; margin: 0; padding: 25px; }}
        .header {{ display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #334155; padding-bottom: 15px; margin-bottom: 25px; }}
        .header h1 {{ margin: 0; font-size: 26px; color: #f8fafc; }}
        .header p {{ margin: 5px 0 0 0; color: #94a3b8; font-size: 14px; }}
        .kpi-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 30px; }}
        .kpi-card {{ background: #1e293b; padding: 20px; border-radius: 12px; border: 1px solid #334155; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); }}
        .kpi-title {{ font-size: 13px; font-weight: 600; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.5px; }}
        .kpi-val {{ font-size: 30px; font-weight: 700; color: #38bdf8; margin-top: 8px; }}
        .kpi-danger {{ color: #ef4444 !important; }}
        .charts-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 30px; }}
        .chart-box {{ background: #1e293b; padding: 20px; border-radius: 12px; border: 1px solid #334155; }}
        .detail-box {{ background: #1e293b; padding: 20px; border-radius: 12px; border: 1px solid #334155; }}
        .detail-box h3 {{ margin-top: 0; color: #38bdf8; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 15px; text-align: left; font-size: 14px; }}
        th {{ background: #0f172a; padding: 12px; color: #94a3b8; border-bottom: 2px solid #334155; }}
        td {{ padding: 12px; border-bottom: 1px solid #334155; }}
        .badge {{ padding: 4px 8px; border-radius: 6px; font-size: 12px; font-weight: 600; }}
        .badge.high-risk {{ background: #7f1d1d; color: #fca5a5; }}
        .badge.standard {{ background: #1e3a8a; color: #93c5fd; }}
        .badge.premium {{ background: #065f46; color: #6ee7b7; }}
        .badge.status-declined {{ background: #991b1b; color: #fecaca; }}
        .badge.status-approved {{ background: #166534; color: #bbf7d0; }}
    </style>
</head>
<body>
    <div class="header">
        <div>
            <h1>TechPay — Executive Risk & Fraud Dashboard</h1>
            <p>Painel de Controle Executivo de Prevenção à Fraude | Base Avaliação (30.000 Transações)</p>
        </div>
        <div style="background:#1e293b; padding:10px 15px; border-radius:8px; border:1px solid #334155; font-size:13px; color:#94a3b8;">
            Status: <span style="color:#22c55e; font-weight:bold;">Ativo / Atualizado</span>
        </div>
    </div>

    <!-- 1. BLOCO KPI -->
    <div class="kpi-grid">
        <div class="kpi-card">
            <div class="kpi-title">Total de Transações</div>
            <div class="kpi-val">{int(kpi['total_tx']):,}</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-title">Volume Financeiro Total</div>
            <div class="kpi-val">R$ {kpi['vol_total']:,.2f}</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-title">Total de Transações Fraudulentas</div>
            <div class="kpi-val kpi-danger">{int(kpi['total_fraudes']):,}</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-title">Taxa de Fraude (%) & Perda Estimada</div>
            <div class="kpi-val kpi-danger">R$ {kpi['perda_fraude']:,.2f} <span style="font-size:18px; color:#f8fafc;">({kpi['taxa_fraude']}%)</span></div>
        </div>
    </div>

    <!-- 2 & 3. BLOCOS DE TENDÊNCIA E COMPOSIÇÃO -->
    <div class="charts-grid">
        <div class="chart-box">
            {fig_trend.to_html(full_html=False, include_plotlyjs='cdn')}
        </div>
        <div class="chart-box">
            {fig_comp.to_html(full_html=False, include_plotlyjs='cdn')}
        </div>
    </div>

    <!-- 4. BLOCO DE DETALHE -->
    <div class="detail-box">
        <h3>Detalhe Operacional: Top 10 Transações com Maior Risco de Fraude</h3>
        <table>
            <thead>
                <tr>
                    <th>ID Transação</th>
                    <th>Cliente</th>
                    <th>Segmento</th>
                    <th>Canal</th>
                    <th>Categoria</th>
                    <th>Valor (R$)</th>
                    <th>Risk Score</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
                {table_rows}
            </tbody>
        </table>
    </div>
</body>
</html>
"""
    with open(out_html, "w", encoding="utf-8") as f:
        f.write(html)
        
    print(f"[OK] Dashboard HTML executivo gerado em '{out_html}'")

if __name__ == "__main__":
    main()
