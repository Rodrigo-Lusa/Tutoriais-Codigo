## ⭐ O que você mais usa

> Contagem automática em ~130 arquivos (`.py`, `.ipynb`, `.sh`) de argos,
> Mestrado, ml_isolados_brasileiros, scripts e Tutoriais-Codigo (out/2026).

### Python — bibliotecas
| Biblioteca | Projetos | Pra quê |
|---|---|---|
| pandas | todos | tabela de resistoma, metadados |
| pathlib | todos | caminhos (`Path.cwd()`, `/`, `glob`, `mkdir`) |
| matplotlib + seaborn | Mestrado, argos, ML | figuras de pôster/dissertação |
| sklearn | ML | classificação, regressão, clustering |
| numpy, scipy | Mestrado, argos, ML | `np.where`, testes estatísticos, distâncias |
| argparse / typer | Mestrado, Tutoriais / argos | CLI de script / CLI do argos |
| json, re | todos | parâmetros, parsing de nomes de gene |
| streamlit | ML | app de resultados |

### pandas — top métodos
| Método | Usos | | Método | Usos |
|---|---|---|---|---|
| `.groupby` | 143 | | `.reindex` | 63 |
| `.isin` | 91 | | `.agg` | 46 |
| `.copy` | 86 | | `.sort_values` | 37+ |
| `.value_counts` | 74 | | `.map` | 51 |
| `.round` | 63 | | `.astype` | 58 |
| `.head` | 86 | | `pd.crosstab` | 20 |

Contexto típico: `resistome.groupby(["sample_id", "drug_class"]).size().unstack(fill_value=0).reindex(ordem)`.

### Gráficos
`plt.subplots` + `plt.tight_layout` (54), `ax.text`, `ax.legend`, `ax.set_*`, `sns.heatmap`, `sns.boxplot`, `ax.add_patch`.

### Bash
| Construção | Usos |
|---|---|
| `$(...)` | 120 |
| `log` / `log_error` (lib/checks.sh) | 150+ |
| `set -euo pipefail` / `set -uo pipefail` | 27 |
| GNU `parallel` | 25 |
| `dirname` / `basename` | 33 |
| `find`, `awk`, `head`, `wc` | 13–17 cada |
| `conda activate`, `docker` | 7 / 12 |
| `${base%.*}`, `${VAR:-padrão}` | vários |
