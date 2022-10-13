from typing import Optional

from sqlmodel import Field, SQLModel
from pydantic import EmailStr, validator
import re

cnpj_regex = re.compile(r'^\d{2}\.\d{3}\.\d{3}\/\d{4}\-\d{2}$')


class EmpresaIn(SQLModel):
    nome: str
    ie: str
    cnpj: str

    @validator("cnpj", pre=True)
    def validate_state(cls, v):
        if not cnpj_regex.search(v):
            raise ValueError("Invalid cnpj")
        return v


class DadosIn(SQLModel):
    da_solicit: Optional[int] = Field(default=None)
    # divida_ativa: Optional[int] = Field(default=None)
    # t_solicit: Optional[int] = Field(default=None)
