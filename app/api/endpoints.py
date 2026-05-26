from numbers import Number

from services.context import construir_dados_completos
from fastapi import APIRouter, HTTPException, BackgroundTasks
from models.schemas import PrevisaoInput, PrevisaoOutput
from ml.inference import modelo_preditor
from ml.trainer import treinamento_automatico

router = APIRouter()

@router.post("/prever", response_model=PrevisaoOutput)
def fazer_previsao(dados: PrevisaoInput):
    produto = dados.produto
    data = dados.data

    dados_enriquecidos = construir_dados_completos(produto, data)

    resultado = modelo_preditor.prever(dados_enriquecidos)

    return resultado

def rotina_treinamento():
    try:
        print("Iniciando rotina de treinamento...");
        sucesso = treinamento_automatico()

        if sucesso:
            modelo_preditor.carregar_todos_modelos()
            print("Memória da API atualizada com sucesso!")

    except Exception as e:
        print(f"Erro durante o treinamento: {e}")

@router.post("/treinar")
def disparar_treinamento(background_tasks: BackgroundTasks):
    background_tasks.add_task(rotina_treinamento)
    return {
        "status": 200,
        "mensagem": "O modelo começou a ser treinado"
    }