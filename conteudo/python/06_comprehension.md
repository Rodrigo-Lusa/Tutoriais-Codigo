## Dict e List Comprehension

### List comprehension — sintaxe
```python
# forma tradicional
lista = []
for x in range(10):
    if x % 2 == 0:
        lista.append(x * 2)

# comprehension equivalente
lista = [x * 2 for x in range(10) if x % 2 == 0]
#         ^valor   ^iteração        ^filtro (opcional)
```

### Dict comprehension — sintaxe (já estava no caderno)
```python
dict_novo = {chave: valor for (chave, valor) in iteravel}

# Exemplo: inverter um dicionário (valor vira chave)
mapa = {'V1': 'Variante1', 'V2': 'Variante2'}
mapa_invertido = {v: k for k, v in mapa.items()}
# {'Variante1': 'V1', 'Variante2': 'V2'}
```

### Onde isso aparece de fato no ARGOS
```python
# Contar quantos genes caem em cada Rank (arg_ranker), a partir da tabela de lookup
# Em vez de um loop com if/elif pra cada Rank:
contagem_por_rank = {
    rank: (df['Rank'] == rank).sum()
    for rank in df['Rank'].unique()
}

# Montar um dicionário sample -> caminho do arquivo de output, pra iterar no update()
arquivos_por_sample = {
    sample: Path(pasta_resultados) / f"{sample}_rgi.txt"
    for sample in lista_samples
}

# Filtrar genes de risco alto (Rank I) já achatados numa lista, a partir do dataset
genes_rank1 = [
    gene for gene in dataset.full_resistoma['gene']
    if rank_lookup.get(gene) == 'Rank I'
]

# Combinando comprehension com o padrão de "matriz na granularidade mais fina":
# construir o dict de renomeação gene_clean -> nome ARO cru, aplicado só na hora
# de plotar (groupby), sem alterar a matriz original
gene_clean_map = {
    aro: aro.split('_')[0]
    for aro in dataset.full_resistoma['gene'].unique()
}
```

### Comprehension aninhada — cuidado com legibilidade
```python
# Achatando uma lista de listas (ex: genes por amostra -> lista única de genes)
genes_por_amostra = [['blaKPC', 'blaNDM'], ['blaOXA'], ['blaKPC']]
todos_genes = [gene for sublist in genes_por_amostra for gene in sublist]
# ['blaKPC', 'blaNDM', 'blaOXA', 'blaKPC']

# Regra prática: se a comprehension passa de ~2 níveis (2 "for") ou fica difícil
# de ler numa linha, é melhor voltar pro loop tradicional — comprehension é
# sobre legibilidade, não sobre economizar linhas.
```

### Set comprehension (bônus — pra valores únicos)
```python
genes_unicos = {gene for sublist in genes_por_amostra for gene in sublist}
# {'blaKPC', 'blaNDM', 'blaOXA'}  -> sem repetição, sem ordem garantida
```
