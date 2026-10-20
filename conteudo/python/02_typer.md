## Typer — CLI (alternativa mais moderna ao argparse)

> `pip install typer`. Usa type hints da função pra gerar o parser automaticamente
> — menos código repetido que argparse pra CLIs simples.

### Básico
```python
import typer

app = typer.Typer()

@app.command()
def saudacao(nome: str, vezes: int = 2):
    """Imprime uma saudação `vezes` vezes."""
    for _ in range(vezes):
        typer.echo(f"Olá, {nome}!")

if __name__ == "__main__":
    app()
```
```bash
python script.py rodrigo            # usa o default vezes=2
python script.py rodrigo --vezes 1
python script.py --help             # help gerado automaticamente
```

### Argumento opcional com `Optional` e flags booleanas
```python
from typing import Optional
import typer

app = typer.Typer()

@app.command()
def processar(
    arquivo: str,
    saida: Optional[str] = None,     # opcional, default None
    verbose: bool = False,           # vira flag: --verbose / --no-verbose
):
    saida = saida or f"{arquivo}_processado.csv"
    if verbose:
        typer.echo(f"Processando {arquivo} -> {saida}")
    ...
```
```bash
python script.py dados.csv --verbose
python script.py dados.csv --saida final.csv
```

### Múltiplos comandos no mesmo app (bom pra CLI de pipeline/toolkit)
```python
import typer

app = typer.Typer()

@app.command()
def rodar(sample: str):
    """Roda a análise pra uma amostra."""
    typer.echo(f"Rodando {sample}")

@app.command()
def status(sample: str):
    """Checa o status de uma amostra já processada."""
    typer.echo(f"Status de {sample}: ok")

if __name__ == "__main__":
    app()
```
```bash
python script.py rodar MAF1
python script.py status MAF1
python script.py --help          # lista os dois comandos
python script.py rodar --help    # help específico do comando
```

### Validação e choices (equivalente ao `choices=` do argparse)
```python
from enum import Enum
import typer

class Formato(str, Enum):
    csv = "csv"
    tsv = "tsv"
    parquet = "parquet"

@app.command()
def exportar(arquivo: str, formato: Formato = Formato.csv):
    typer.echo(f"Exportando como {formato.value}")
```
```bash
python script.py exportar dados        # usa csv (default)
python script.py exportar dados --formato parquet
python script.py exportar dados --formato xml   # erro: não é uma opção válida
```

### Path como tipo (valida e converte automaticamente)
```python
from pathlib import Path
import typer

@app.command()
def carregar(arquivo: Path):
    if not arquivo.exists():
        typer.echo(f"Arquivo não encontrado: {arquivo}", err=True)
        raise typer.Exit(code=1)
    typer.echo(f"Carregando {arquivo}")
```
