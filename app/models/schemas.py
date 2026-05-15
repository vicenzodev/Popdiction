from pydantic import BaseModel

class PrevisaoInput(BaseModel):
    temp_min_semana: float
    temp_max_semana: float
    temp_media_semana: float
    umidade_media_semana: float
    tem_feriado_na_semana: int
    vendas_semana_passada: float # <-- Alterado aqui
    mes: int
    semana_do_ano: int

class PrevisaoOutput(BaseModel):
    qtd: float # <-- Apenas uma saída