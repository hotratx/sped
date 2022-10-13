import typer
from rich import print
from new_sped.db.databases import create_db
from new_sped.db.crud import Crud
from new_sped.scripts import sped

app = typer.Typer(rich_markup_mode="rich")


@app.command(help="[bold red]Vai rodar o sped[/bold red]")
def call_sped():
    """Roda o sped"""
    print('CALL sped')
    # sped()


@app.command(help="[bold blue]Vai rodar o cert_pi[/bold blue]")
def call_cert_pi():
    """Roda o cert_pi"""
    print('CALL cert_pi')
    # cert_pi()

# crud = Crud()
# crud.create_empresa('Matheus', '12341234', '123')
# x = crud.get_empresas()
# print(f'EMPRESAS: {x}')

if __name__ == "__main__":
    # create_db()
    app()
