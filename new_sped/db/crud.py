from .models import Empresa, Dado
from .databases import engine
from .schemas import EmpresaIn, DadosIn
from sqlmodel import Session, select


class Crud:
    def create_empresa(self, emp: EmpresaIn) -> None:
        db_emp = Empresa.from_orm(emp)
        with Session(engine) as session:
            session.add(db_emp)
            session.commit()
            session.refresh(db_emp)

    def create_dados(self, data: DadosIn, emp: Empresa):
        db_data = Dado.from_orm(data)
        db_data.empresa = emp
        # dado = Dado(da_solicit=da_solicit, empresa=emp)
        with Session(engine) as session:
            session.add(db_data)
            session.commit()
            session.refresh(db_data)

    def get_empresas(self) -> list[Empresa]:
        stmt = select(Empresa)
        with Session(engine) as session:
            results = session.exec(stmt).all()
            return results
