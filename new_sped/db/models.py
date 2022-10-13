from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class Empresa(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str = Field(index=True)
    ie: str
    cnpj: str
    dados: List["Dado"] = Relationship(back_populates="empresa")


class Dado(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    da_solicit: Optional[int] = Field(default=None)
    # divida_ativa: Optional[int] = Field(default=None)
    # t_solicit: Optional[int] = Field(default=None)
    empresa_id: Optional[int] = Field(default=None, foreign_key="empresa.id")
    empresa: Optional[Empresa] = Relationship(back_populates="dados")
