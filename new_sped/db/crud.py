from new_sped.db.models import Empresa, Usuario, Cert_pi, Sped_send, Sped_error
from new_sped.db.databases import engine
from new_sped.db.schemas import EmpresaIn, UsuariosIn, Cert_piIn, Sped_sendIn, Sped_errorIn
from sqlmodel import Session, select


class Crud:
    def create_empresa(self, emp: EmpresaIn) -> None:
        db_emp = Empresa.from_orm(emp)
        with Session(engine) as session:
            session.add(db_emp)
            session.commit()
            session.refresh(db_emp)

    def create_usuarios(self, user: UsuariosIn, emp: Empresa):
        db_user = Usuario.from_orm(user)
        db_user.empresas = [emp]
        with Session(engine) as session:
            session.add(db_user)
            session.commit()
            session.refresh(db_user)

    def create_dados1(self, data: Cert_piIn, emp: Empresa):
        db_data = Cert_pi.from_orm(data)
        db_data.empresa = emp
        with Session(engine) as session:
            session.add(db_data)
            session.commit()
            session.refresh(db_data)

    def create_dados2(self, data: Sped_sendIn, emp: Empresa):
        db_data = Sped_send.from_orm(data)
        db_data.empresa = emp
        with Session(engine) as session:
            session.add(db_data)
            session.commit()
            session.refresh(db_data)

    def create_dados3(self, data: Sped_errorIn, emp: Empresa):
        db_data = Sped_error.from_orm(data)
        db_data.empresa = emp
        with Session(engine) as session:
            session.add(db_data)
            session.commit()
            session.refresh(db_data)

    def get_empresas(self):
        stmt = select(Empresa.cnpj)
        with Session(engine) as session:
            results = session.exec(stmt).all()
            return results
