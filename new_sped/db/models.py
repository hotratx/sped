from datetime import datetime
from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel


class UserEmpresasLink(SQLModel, table=True):
    user_id: Optional[int] = Field(default=None, foreign_key="usuario.id", primary_key=True)
    emp_id: Optional[int] = Field(default=None, foreign_key="empresa.id", primary_key=True)


class Usuario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str = Field(index=True)
    cpf: str = Field(index=True, unique=True)  
    empresas: List["Empresa"] = Relationship(back_populates="usuarios", link_model=UserEmpresasLink)


class Empresa(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str = Field(index=True)
    ie: str = Field(index=True, unique=True)
    cnpj: str = Field(index=True, unique=True)
    usuarios: List[Usuario] = Relationship(back_populates="empresas", link_model=UserEmpresasLink)
    dados1: List["Cert_pi"] = Relationship(back_populates="empresa")
    dados2: List["Sped_send"] = Relationship(back_populates="empresa")


class Cert_pi(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    da_solicit: str
    da_value: str
    t_solicit: str
    t_value: str
    empresa_id: Optional[int] = Field(default=None, foreign_key="empresa.id")
    empresa: Optional[Empresa] = Relationship(back_populates="dados1")


class Sped_send(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    period: datetime
    date_send: datetime
    send: str
    stats: str
    empresa_id: Optional[int] = Field(default=None, foreign_key="empresa.id")
    empresa: Optional[Empresa] = Relationship(back_populates="dados2")


class Sped_error(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    group: str
    type: str
    inconsis: str
    empresa_id: Optional[int] = Field(default=None, foreign_key="empresa.id")
    empresa: Optional[Empresa] = Relationship(back_populates="dados3")

