import joblib
import pandas as pd
from app.core.config import settings

class ModeloPrevisao:
    def __init__(self):
        self.modelo = None
        self.carregar_modelo()

    def carregar_modelo(self):
        try:
            self.modelo = joblib.load(settings.MODEL_PATH)
            print("Modelo carregado com sucesso!")
        except FileNotFoundError:
            print(f"Erro: Modelo não encontrado no caminho {settings.MODEL_PATH}")

    def prever(self, dados_entrada: dict) -> dict:
        if not self.modelo:
            raise ValueError("O modelo não está carregado.")

        # Transforma o dicionário recebido da API em um DataFrame de 1 linha
        df_entrada = pd.DataFrame([dados_entrada])
        
        # Faz a predição
        resultado = self.modelo.predict(df_entrada)

        # Mapeia a saída do RandomForest para o nosso Schema
        return {
            "qtd_leitinho_5l": round(resultado, 2)
        }

# Instância global para carregar o modelo apenas uma vez quando a API iniciar
modelo_preditor = ModeloPrevisao()