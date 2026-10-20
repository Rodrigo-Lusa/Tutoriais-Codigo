## Numpy, Matplotlib e Seaborn

### Numpy — o essencial
```python
import numpy as np

arr = np.array([1, 2, 3, 4, 5])
arr.shape                       # dimensões
arr.mean(); arr.std(); arr.sum()
np.log2(arr)                    # bom pra fold-change
np.log10(arr + 1)               # +1 evita log(0)

# Arrays 2D (tipo uma matrix de presença/ausência)
matrix = np.zeros((5, 3))       # matriz de zeros 5x3
matrix = np.ones((5, 3))
np.where(arr > 2, 'alto', 'baixo')   # vetorizado, equivalente a apply(lambda) linha a linha

# Random (pra simulação/teste)
np.random.seed(42)              # reprodutibilidade
np.random.normal(0, 1, size=100)
```

### Matplotlib — parâmetros completos por tipo de gráfico

Setup básico:
```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(8, 5), dpi=100)
# figsize=(largura, altura) em polegadas; dpi = resolução

ax.set_title('Título', fontsize=14)
ax.set_xlabel('Eixo X')
ax.set_ylabel('Eixo Y')
ax.legend(loc='best')           # 'upper right', 'lower left', 'best', etc.
plt.tight_layout()              # evita corte de labels
plt.savefig('figura.png', dpi=300, bbox_inches='tight')
plt.show()
```

**Scatter**
```python
ax.scatter(
    x, y,
    c=cores,              # cor por ponto (array numérico ou lista de cores)
    s=tamanhos,            # tamanho por ponto (array ou valor único)
    cmap='viridis',        # paleta, usada só se c for numérico
    alpha=0.7,             # transparência (0-1)
    edgecolors='black',
    linewidths=0.5,
    marker='o',            # 'o', 's', '^', 'x', 'D', etc.
)
```

**Bar**
```python
ax.bar(
    x, altura,
    width=0.8,
    color='steelblue',     # ou lista de cores, uma por barra
    edgecolor='black',
    linewidth=0.5,
    align='center',        # 'center' ou 'edge'
    yerr=erros,            # barra de erro (opcional)
    capsize=4,
)
```

**Line**
```python
ax.plot(
    x, y,
    color='crimson',
    linestyle='-',          # '-', '--', '-.', ':'
    linewidth=2,
    marker='o',
    markersize=5,
    label='LFQ médio',
)
```

**Boxplot**
```python
ax.boxplot(
    [grupo1, grupo2, grupo3],
    labels=['A', 'B', 'C'],
    showfliers=True,        # mostrar outliers
    patch_artist=True,      # permite colorir as caixas
)
```

**Heatmap "cru" (imshow)**
```python
im = ax.imshow(matrix, cmap='viridis', aspect='auto', vmin=0, vmax=1)
plt.colorbar(im, ax=ax, label='valor')
```

### Compondo e ajustando o gráfico

**Adicionar linhas a um gráfico já existente** — chame `ax.plot`/`ax.axhline`/`ax.axvline`
de novo no mesmo `ax`, sem criar uma figura nova:
```python
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(x, y1, label='Amostra A')
ax.plot(x, y2, label='Amostra B')          # segunda linha, mesmo eixo

# Linhas de referência (ex: threshold de significância)
ax.axhline(y=0.05, color='red', linestyle='--', linewidth=1, label='p = 0.05')
ax.axvline(x=0, color='gray', linestyle=':', linewidth=1)

# Linha diagonal genérica (ex: y=x numa comparação)
ax.axline((0, 0), slope=1, color='black', linestyle='--', linewidth=0.8)

ax.legend()
```

**Mudar título e "proporção" do gráfico**
```python
ax.set_title('Novo título', fontsize=14, fontweight='bold')
fig.suptitle('Título geral da figura', fontsize=16)   # quando tem vários subplots

# Proporção/tamanho da figura inteira
fig, ax = plt.subplots(figsize=(10, 4))    # largura maior que altura -> mais "wide"
fig, ax = plt.subplots(figsize=(6, 6))     # quadrado

# Proporção dos EIXOS dentro do gráfico (não da figura)
ax.set_aspect('equal')       # 1 unidade em x = 1 unidade em y (bom pra PCoA/PCA)
ax.set_aspect('auto')        # padrão, deixa esticar livremente
ax.set_aspect(2)             # y comprimido/esticado 2x em relação a x
```

**Mudar a posição da legenda**
```python
ax.legend(loc='upper right')     # 'upper left', 'upper right', 'lower left',
                                  # 'lower right', 'center', 'best', etc.

# Legenda FORA do gráfico (bbox_to_anchor + loc controlam o ponto de ancoragem)
ax.legend(loc='center left', bbox_to_anchor=(1.02, 0.5))   # à direita, fora do plot
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3)  # embaixo, em linha

# Outros ajustes úteis
ax.legend(title='Grupo', frameon=False, fontsize=9)
```

**Subplots — plotar um do lado do outro**
```python
# 1 linha, 2 colunas -> lado a lado
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
axes[0].scatter(x1, y1)
axes[0].set_title('Clínico')
axes[1].scatter(x2, y2)
axes[1].set_title('Ambiental')
plt.tight_layout()

# 2 linhas, 2 colunas -> grade 2x2 (indexa como matrix)
fig, axes = plt.subplots(2, 2, figsize=(10, 8))
axes[0, 0].plot(x, y)
axes[0, 1].bar(x, y)
axes[1, 0].boxplot(dados)
axes[1, 1].imshow(matrix)

# sharex/sharey -> eixos compartilhados entre os subplots (bom pra comparação direta)
fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharey=True)
```

### Seaborn — parâmetros completos por tipo de gráfico

Setup:
```python
import seaborn as sns
sns.set_theme(style='whitegrid')   # 'white', 'dark', 'darkgrid', 'ticks'
```

**Heatmap** (o mais usado no ARGOS)
```python
sns.heatmap(
    matrix,
    cmap='viridis',          # paleta (ver seção 2.2.5)
    annot=True,               # mostra o valor em cada célula
    fmt='.2f',                 # formato do número anotado
    linewidths=0.5,
    linecolor='white',
    vmin=0, vmax=1,             # limites da escala de cor
    cbar_kws={'label': 'valor'},
    square=False,
    xticklabels=True,
    yticklabels=True,
)
```

**Clustermap** (heatmap + dendrograma — equivalente ao `clustered_heatmap` do ARGOS)
```python
sns.clustermap(
    matrix,
    cmap='viridis',
    metric='jaccard',        # ou 'braycurtis', 'euclidean'...
    method='average',         # linkage: 'average', 'complete', 'ward'
    row_cluster=True,
    col_cluster=True,
    figsize=(10, 10),
    annot=False,
)
```

**Barplot / Boxplot / Violinplot**
```python
sns.barplot(data=df, x='Amostra', y='LFQ', hue='drug_class', palette='Set2', errorbar='sd')
sns.boxplot(data=df, x='Amostra', y='LFQ', hue='tipo', palette='pastel')
sns.violinplot(data=df, x='Amostra', y='LFQ', palette='muted', inner='quartile')
```

**Scatterplot**
```python
sns.scatterplot(
    data=df, x='logFC', y='-log10(p)',
    hue='sig',               # colore por categoria
    style='drug_class',       # muda o marcador por categoria
    size='LFQ',                # tamanho do ponto por valor
    palette='coolwarm',
    alpha=0.7,
)
```

**Pairplot** (bom pra EDA — ver seção 2.7)
```python
sns.pairplot(df, hue='tipo', palette='husl', diag_kind='kde')
```

**Seaborn + subplots** — funções `sns.*plot` aceitam `ax=` pra desenhar dentro de um
subplot específico do matplotlib:
```python
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
sns.boxplot(data=df, x='tipo', y='LFQ', ax=axes[0])
sns.violinplot(data=df, x='tipo', y='LFQ', ax=axes[1])
```

### Paletas de cores prontas
```python
# Contínuas / sequenciais (valores numéricos, ex: heatmap, LFQ)
'viridis'      # padrão robusto, perceptualmente uniforme
'magma' / 'inferno' / 'plasma'   # variações escuro->claro
'Blues' / 'Greens' / 'Reds'       # sequenciais de uma cor só

# Divergentes (valores com ponto central, ex: log2FC, correlação)
'coolwarm'
'RdBu_r'       # vermelho-azul, invertido pra vermelho = positivo
'vlag'

# Categóricas (grupos discretos, ex: Amostra, drug_class)
'Set1' / 'Set2' / 'Set3'
'tab10' / 'tab20'
'husl'         # cores igualmente espaçadas, boa quando tem muitas categorias
'pastel' / 'muted' / 'deep' / 'bright'   # variações de saturação do seaborn

# Definir manualmente (quando quer controlar cor exata por grupo)
paleta_manual = {'clinico': '#d62728', 'ambiental': '#2ca02c'}
sns.boxplot(data=df, x='tipo', y='LFQ', palette=paleta_manual)
```
