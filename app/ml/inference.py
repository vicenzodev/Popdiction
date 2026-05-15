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

        df_entrada = pd.DataFrame([dados_entrada])
        
        # O resultado agora é apenas um número
        resultado = self.modelo.predict(df_entrada)[0]

        return {
            "qtd": round(resultado, 2)
        }

modelo_preditor = ModeloPrevisao()