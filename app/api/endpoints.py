from fastapi import APIRouter, HTTPException
from app.models.schemas import PrevisaoInput, PrevisaoOutput
from app.ml.inference import modelo_preditor

router = APIRouter()

@router.post("/prever", response_model=PrevisaoOutput)
def fazer_previsao(dados: PrevisaoInput):
    try:
        # Pega os dados validados do Pydantic e converte para dicionário
        dados_dict = dados.model_dump()
        
        # Envia para a camada de ML fazer a mágica
        resultado = modelo_preditor.prever(dados_dict)
        
        return resultado
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar predição: {str(e)}")