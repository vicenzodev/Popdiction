from pydantic import BaseModel

# Formato dos dados que a API vai receber (Input)
class PrevisaoInput(BaseModel):
    temp_min_semana: float
    temp_max_semana: float
    temp_media_semana: float
    umidade_media_semana: float
    tem_feriado_na_semana: int
    vendas_leitinho_semana_passada: float
    vendas_flocos_semana_passada: float
    vendas_frutao_semana_passada: float
    mes: int
    semana_do_ano: int

# Formato dos dados que a API vai devolver (Output)
class PrevisaoOutput(BaseModel):
    qtd: float