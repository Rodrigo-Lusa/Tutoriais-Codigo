## Estatística com scipy

> O que você usa: `chi2_contingency` (tabela de contingência, ex: classe de
> droga × bioma), `mannwhitneyu`/`kruskal` (comparar distribuições sem supor
> normalidade), `spearmanr`, `ttest_ind`, `levene`, `ks_2samp`, `chisquare`, `pdist`.

### Qual teste usar?
| Pergunta | Dados | Teste |
|---|---|---|
| 2 categóricas estão associadas? | tabela de contagem | `chi2_contingency(pd.crosstab(a, b))` |
| frequências observadas batem com o esperado? | 1 vetor de contagem | `chisquare(obs, f_exp)` |
| 2 grupos têm a mesma média? | numérico, ~normal | `ttest_ind(g1, g2, equal_var=False)` |
| 2 grupos, sem supor normalidade | numérico/ordinal | `mannwhitneyu(g1, g2)` ⭐ |
| 3+ grupos, sem supor normalidade | numérico/ordinal | `kruskal(*grupos)` |
| variâncias iguais? | numérico | `levene(g1, g2)` |
| distribuições iguais? | numérico | `ks_2samp(g1, g2)` |
| correlação monotônica | 2 numéricos | `spearmanr(x, y)` ⭐ |
| correlação linear | 2 numéricos | `pearsonr(x, y)` |
| é normal? | numérico | `shapiro(x)` |

### Exemplos
```python
from scipy import stats
from scipy.stats import chi2_contingency, mannwhitneyu, kruskal, spearmanr

# Qui-quadrado: risco × bioma
tab = pd.crosstab(df["bioma"], df["Risco"])
chi2, p, dof, esperado = chi2_contingency(tab)
print(f"chi2={chi2:.2f}, p={p:.3g}, gl={dof}")      # esperado < 5 em muitas células -> cuidado

# Mann-Whitney: nº de ARGs em plasmídeo vs cromossomo
stat, p = mannwhitneyu(df.loc[df.tipo == "plasmid", "n_args"],
                       df.loc[df.tipo == "chromosome", "n_args"],
                       alternative="two-sided")

# Kruskal com grupos vindos de um groupby
grupos = [g["n_args"].values for _, g in df.groupby("bioma")]
stat, p = kruskal(*grupos)

# Spearman
rho, p = spearmanr(df["n_genes"], df["n_plasmideos"])

# Distância entre amostras (base da PCoA / clustering hierárquico)
from scipy.spatial.distance import pdist, squareform
D = squareform(pdist(matriz_presenca, metric="jaccard"))   # 'braycurtis' pra contagem
```

### Correção pra múltiplos testes
```python
from statsmodels.stats.multitest import multipletests
rej, p_ajust, _, _ = multipletests(lista_p, alpha=0.05, method="fdr_bh")   # Benjamini-Hochberg
```

### Função de interpretação (padrão do `Regression.__interpretar`)
```python
def interpretar(nome, stat, p, alfa=0.05):
    conclusao = "rejeita H0" if p < alfa else "não rejeita H0"
    print(f"{nome}: estat={stat:.3f}, p={p:.3g} -> {conclusao} (α={alfa})")
```
