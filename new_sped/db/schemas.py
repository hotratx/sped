from datetime import date
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


class UsuariosIn(SQLModel):
    nome: Optional[str] = Field(default=None)
    cpf: Optional[str] = Field(default=None)


class Cert_piIn(SQLModel):
    da_solicit: Optional[str] = Field(default=None)
    da_value: Optional[str] = Field(default=None)
    t_solicit: Optional[str] = Field(default=None)
    t_value: Optional[str] = Field(default=None)


class Sped_sendIn(SQLModel):
    period: Optional[date] = Field(default=None)
    date_send: Optional[date] = Field(default=None)
    send: Optional[str] = Field(default=None)
    stats: Optional[str] = Field(default=None)


class Sped_errorIn(SQLModel):
    group: Optional[str] = Field(default=None)
    type: Optional[str] = Field(default=None)
    inconsis: Optional[str] = Field(default=None)
