from pydantic import BaseModel

class PrevisaoInput(BaseModel):
    produto: str
    data:str

class PrevisaoOutput(BaseModel):
    qtd: float
    mae: float 
    rmae: float 

class HistoricoInput(BaseModel):
    data: str
    loja: str
    cidade: str
    produto: str
    qtd: float

class ImportacaoOutput(BaseModel):
    status: int
    mensagem: str
    registros_inseridos: int
    duplicatas_removidas: int

class TreinamentoInput(BaseModel):
    caminho_arquivo: str