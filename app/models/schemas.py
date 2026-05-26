from pydantic import BaseModel

class PrevisaoInput(BaseModel):
    produto: str
    data:str

class PrevisaoOutput(BaseModel):
    qtd: float

class TreinamentoInput(BaseModel):
    caminho_arquivo: str