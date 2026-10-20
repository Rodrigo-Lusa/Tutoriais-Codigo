## Python essenciais (argparse + pathlib, do zip)

> Consolidado de `python/argparse.py` e `python/pathlib.py`. `argparse` é a
> alternativa mais antiga/verbosa ao typer (seção 2.5) — útil saber ler, mesmo
> usando typer pra escrever CLIs novas.

### argparse — básico
```python
import argparse

parser = argparse.ArgumentParser()

# Argumento posicional (obrigatório, sem --)
parser.add_argument('greeting', type=str, help='The greeting message to display')

# Argumento opcional (com -- ou -)
parser.add_argument('-t', '--times', type=int, help='Number of times to display the greeting')
parser.set_defaults(times=2)

args = parser.parse_args()

for i in range(args.times):
    print(args.greeting)
```
```bash
python teste_arg.py oi
# oi
# oi
python teste_arg.py oi -t 1
# oi
```

### argparse — choices (restringir valores aceitos)
```python
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('greeting', type=str, help='The greeting message to display')
parser.add_argument('-l', '--language', type=str, choices=['en', 'pt'], help='Language of the greeting')
parser.set_defaults(language='pt')

args = parser.parse_args()

for i in range(args.times):
    if args.language == 'pt':
        print(f"Olá! {args.greeting}")
    else:
        print(f"Hello! {args.greeting}")
```
```bash
python teste_arg.py rodrigo
# Olá! rodrigo
python teste_arg.py rodrigo -l en
# Hello! rodrigo
```

### pathlib — manipulação de caminhos
```python
from pathlib import Path

# Diretório atual
print(Path.cwd())

# Listar tudo no diretório atual
for p in Path().iterdir():
    print(p)

### Manipulando partes do caminho
script = Path("teste_arg.py")
print(script.suffix)   # .py -> só a extensão
print(script.stem)     # teste_arg -> nome sem extensão
print(script.parent)   # . -> diretório pai

### Criar diretório e arquivo
new_dir = Path("diretorio_1")
new_dir.mkdir(exist_ok=True)          # não dá erro se já existir

new_file = new_dir / "novo_arquivo.txt"
print(new_file.absolute())
new_file.touch(exist_ok=True)

### Caminhos relativos, absolutos e home
Path("..").absolute()      # caminho absoluto sem resolver ".."
Path("..").resolve()       # resolve ".." e links simbólicos
Path(__file__).resolve()   # caminho absoluto do próprio script
Path.home()                # diretório home do usuário

### Glob — buscar arquivos por padrão
for p in Path().glob("*.py"):     # só no diretório atual
    print(p)

for p in Path().rglob("*.py"):    # recursivo (subpastas também)
    print(p)

### Ler e escrever arquivos
arquivo = Path.home() / "testes/teste_arg.py"
with arquivo.open() as f:
    print(f.read())
```

### json — ler/escrever dicionário em arquivo
```python
import json
from pathlib import Path

params = {"modelo": "rf", "n_splits": 5, "features": ["n_args", "n_plasmid"]}
Path("params.json").write_text(json.dumps(params, indent=2, ensure_ascii=False))   # ensure_ascii=False mantém acento
params = json.loads(Path("params.json").read_text())

json.dumps(obj, default=str)      # default=str converte o que o json não entende (Path, set, datetime)
```

### re — expressões regulares ⭐
```python
import re

m = re.search(r"class ([ABCD]) beta-lactamase", texto, re.IGNORECASE)
if m:
    m.group(0)    # trecho inteiro que casou
    m.group(1)    # 1º grupo entre parênteses -> 'A'

PADRAO = re.compile(r"^(OXA-\d+)-like$")          # compila 1 vez quando for usar muitas vezes
PADRAO.match("OXA-23-like").group(1)              # 'OXA-23'   (match = só no INÍCIO da string)

re.findall(r"SRR\d+", texto)                      # lista de todas as ocorrências
re.sub(r"^bla", "", "blaKPC-2", flags=re.I)       # 'KPC-2'
re.split(r"[;,]\s*", "a; b,c")                    # ['a', 'b', 'c']

# No pandas (mesma regex, vetorizado)
df["gene"].str.contains(r"KPC|NDM", regex=True, na=False)
df["seq_name"] = df["ORF_ID"].str.extract(r"^(\S+)_\d+")        # grupo -> coluna nova
df["gene"].str.replace(r"-like$", "", regex=True)
```
| Símbolo | Significa |
|---|---|
| `.` `\d` `\w` `\s` | qualquer char / dígito / letra-número-_ / espaço |
| `*` `+` `?` `{2,4}` | 0+ / 1+ / 0 ou 1 / entre 2 e 4 |
| `^` `$` | início / fim |
| `[ABC]` `[^ABC]` | um desses / nenhum desses |
| `(...)` `(?:...)` | grupo capturado / grupo sem captura |
| `a\|b` | a ou b |

### sys.argv — script rápido sem argparse
```python
import sys
csv_path, batch_size, out_dir = sys.argv[1], int(sys.argv[2]), Path(sys.argv[3])   # (gerar_lotes.py)
```
