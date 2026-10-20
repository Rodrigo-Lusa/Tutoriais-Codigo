## Notebook + pasta `src/` (o padrão dos seus projetos)

> Notebook pra **explorar e mostrar**; função/classe reaproveitável vai pra
> `src/*.py` e o notebook importa. Assim o mesmo código serve pro notebook,
> pro script e pro app Streamlit.

### Estrutura
```
projeto/
├── data/                 # raw/, processed/
├── notebooks/
│   ├── 01_EDA.ipynb
│   └── src/              # (ou src/ na raiz, como no Mestrado/03_analise)
│       ├── __init__.py   # transforma a pasta em pacote importável
│       ├── paths.py      # ROOT, TABLES, FIGURES... num lugar só
│       └── classifier.py
└── results/
```

### Primeira célula ⭐
```python
%load_ext autoreload
%autoreload 2                 # recarrega src/*.py sozinho quando você edita (sem reiniciar o kernel)

import sys, warnings
from pathlib import Path
import numpy as np, pandas as pd
import matplotlib.pyplot as plt, seaborn as sns

warnings.filterwarnings("ignore", category=FutureWarning)

# acha a raiz subindo pastas até encontrar um marcador -> funciona de qualquer subpasta
ROOT = next(p for p in [Path.cwd(), *Path.cwd().parents] if (p / "parquet_data").exists())
sys.path.insert(0, str(ROOT))   # deixa `from src.x import y` funcionar

from src.paths import TABLES, FIGURES
from src.resistome import annotate_resistome

pd.set_option("display.width", 200)
pd.set_option("display.max_colwidth", 70)
pd.set_option("display.max_rows", 200)
pd.set_option("display.max_columns", None)
```

### `paths.py` — caminhos centralizados
```python
from pathlib import Path

def find_project_root(markers=("parquet_data", "meta")) -> Path:
    here = Path(__file__).resolve().parent
    for folder in [Path.cwd(), *Path.cwd().parents, here, *here.parents]:
        if all((folder / m).exists() for m in markers):
            return folder
    raise FileNotFoundError(f"Could not find {markers} above {Path.cwd()}")

ROOT = find_project_root()
TABLES = ROOT / "results" / "tables"
FIGURES = ROOT / "results" / "figures"
```

### Atalhos que valem ouro
| Atalho / mágica | Faz |
|---|---|
| `Shift+Enter` | roda a célula e desce |
| `Esc` → `A` / `B` | nova célula acima / abaixo |
| `Esc` → `M` / `Y` | vira markdown / código |
| `Esc` → `D D` | apaga a célula |
| `Tab` / `Shift+Tab` | autocompletar / ver assinatura da função |
| `obj?` / `obj??` | docstring / código-fonte |
| `%time cmd` / `%%time` | tempo de uma linha / da célula |
| `!ls data/` | roda comando de shell |
| `%who` | variáveis definidas |
| `display(df)` | mostra mais de uma tabela formatada na mesma célula |

### Salvar resultado do notebook
```python
fig.savefig(FIGURES / "heatmap.png", dpi=300, bbox_inches="tight")
df.to_csv(TABLES / "resumo.tsv", sep="\t", index=False)
df.to_parquet(TABLES / "resumo.parquet")      # mantém tipos, bem menor e mais rápido que csv
(TABLES / "params.json").write_text(json.dumps(params, indent=2))
```
