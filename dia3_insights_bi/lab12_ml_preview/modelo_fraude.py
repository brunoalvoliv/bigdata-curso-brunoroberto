#!/usr/bin/env python3
"""
Lab 12: Modelo Preditivo de Fraude (Preview Machine Learning)
Curso: Big Data para Negócios
"""
import duckdb
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score

def main():
    print("=== Lab 12: Modelo Preditivo de Detecção de Fraudes (scikit-learn) ===")
    con = duckdb.connect()
    silver_path = "bigdata/silver/silver_transactions.parquet"
    
    df = con.sql(f"""
    SELECT amount, credit_score, risk_score, is_madrugada, is_fraud
    FROM '{silver_path}'
    """).df()
    
    X = df[['amount', 'credit_score', 'risk_score', 'is_madrugada']].astype(float)
    y = df['is_fraud'].astype(int)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
    
    model = LogisticRegression(max_iter=1000, class_weight='balanced')
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]
    
    auc = roc_auc_score(y_test, y_proba)
    print(f"[OK] Modelo treinado com sucesso! ROC-AUC Score: {auc:.4f}\n")
    print("Relatório de Classificação:")
    print(classification_report(y_test, y_pred))
    
    features = ['amount', 'credit_score', 'risk_score', 'is_madrugada']
    coefs = pd.DataFrame({'Feature': features, 'Coeficiente': model.coef_[0]}).sort_values(by='Coeficiente', ascending=False)
    print("\nImportância dos Atributos (Coeficientes da Regressão Logística):")
    print(coefs)

if __name__ == "__main__":
    main()
