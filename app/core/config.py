import os

class Settings:
    PROJECT_NAME: str = "API Previsão de Sorvetes"
    VERSION: str = "1.0.0"
    
    # Caminho base para encontrar o modelo salvo
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    MODEL_PATH: str = os.path.join(BASE_DIR, "ml", "modelo_sorvetao_v1.pkl")

settings = Settings()