#!/usr/bin/env python3
"""
Avaliação Final — Etapa 4 (Bônus): Modelo Preditivo de Fraude (Machine Learning)
Treinamento de Regressão Logística com Scikit-Learn sobre avaliacao_transactions.csv
Curso: Big Data para Negócios
"""
import duckdb
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix

def main():
    print("=================================================================")
    print("   ETAPA 4 — MODELO PREDITIVO DE FRAUDE (MACHINE LEARNING)")
    print("=================================================================")
    
    con = duckdb.connect()
    silver_path = "avaliacao_final/etapa2_bigdata/data/silver/silver_transactions.parquet"
    
    df = con.sql(f"""
    SELECT
        amount,
        credit_score,
        risk_score,
        is_madrugada,
        CASE WHEN channel = 'app' THEN 1 ELSE 0 END AS is_channel_app,
        CASE WHEN merchant_category = 'viagem' THEN 1 ELSE 0 END AS is_cat_viagem,
        CASE WHEN segment = 'High-Risk' THEN 1 ELSE 0 END AS is_seg_highrisk,
        is_fraud
    FROM '{silver_path}'
    """).df()
    
    X = df[['amount', 'credit_score', 'risk_score', 'is_madrugada', 'is_channel_app', 'is_cat_viagem', 'is_seg_highrisk']]
    y = df['is_fraud'].astype(int)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=123, stratify=y)
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    model = LogisticRegression(class_weight='balanced', max_iter=1000, random_state=123)
    model.fit(X_train_scaled, y_train)
    
    y_pred = model.predict(X_test_scaled)
    y_proba = model.predict_proba(X_test_scaled)[:, 1]
    
    auc = roc_auc_score(y_test, y_proba)
    print(f"\n[OK] Modelo treinado com sucesso!")
    print(f"Desempenho Global (ROC-AUC Score): {auc:.4f}\n")
    
    print("--- Relatório de Métricas de Classificação ---")
    print(classification_report(y_test, y_pred, target_names=['Legítima (0)', 'Fraude (1)']))
    
    print("\n--- Matriz de Confusão ---")
    cm = confusion_matrix(y_test, y_pred)
    print(f"Verdadeiro Negativo: {cm[0][0]} | Falso Positivo: {cm[0][1]}")
    print(f"Falso Negativo: {cm[1][0]}      | Verdadeiro Positivo: {cm[1][1]}")
    
    features = ['amount', 'credit_score', 'risk_score', 'is_madrugada', 'is_channel_app', 'is_cat_viagem', 'is_seg_highrisk']
    coef_df = pd.DataFrame({
        'Variável': features,
        'Coeficiente (Peso)': model.coef_[0]
    }).sort_values(by='Coeficiente (Peso)', ascending=False)
    
    print("\n--- Importância dos Atributos (Coeficientes do Modelo) ---")
    print(coef_df.to_string(index=False))

if __name__ == "__main__":
    main()
