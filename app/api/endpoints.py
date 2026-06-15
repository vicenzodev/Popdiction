from numbers import Number

from typing import List
from services.context import construir_dados_completos
from services.data_handler import inserir_registros_historico
from fastapi import APIRouter, HTTPException, BackgroundTasks
from models.schemas import PrevisaoInput, PrevisaoOutput, HistoricoInput, ImportacaoOutput
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

@router.post("/historico/importar", response_model=ImportacaoOutput)
def importar_historico(registros: List[HistoricoInput]):
    try:
        resultado = inserir_registros_historico([registro.dict() for registro in registros])
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {
        "status": 200,
        "mensagem": "Dados do histórico importados com sucesso",
        "registros_inseridos": resultado["registros_inseridos"],
        "duplicatas_removidas": resultado["duplicatas_removidas"]
    }

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