## Pandas

### Do caderno (transcrição completa)

**Import e inspeção**
```python
df = pd.read_csv('file')              # csv
df = pd.read_csv('file', sep='\t')    # tsv

df.columns                            # nomes das colunas
df.dtypes                             # tipo de cada coluna
df.describe()                         # estatísticas gerais (numéricas)
```

**Seleção de colunas e filtro**
```python
df['coluna']
df[['coluna1', 'coluna2']]            # lista de colunas

# Filtrar
df[df['Amostra'] == 'MAF1']
df[df['Amostra'].isin(['MAF1', 'MAF2'])]

# And / Or -> sempre com parênteses em cada condição (x | y)
df[(df['LFQ'] > 10) & (df['p'] < 0.05)]

# Texto
df[df['gene'].str.contains('ribosom', case=False)]
```

**Query**
```python
df.query('coluna < 0.05')
df.query('coluna > 8 and tipo < 6')
```

**Valores únicos**
```python
df['Amostra'].unique()                # lista
df['Amostra'].nunique()               # int
df['Amostra'].value_counts()
df['Amostra'].value_counts(normalize=True)
df['Amostra'].value_counts().to_dict()
```

**Ordenação**
```python
df.sort_values('LFQ', ascending=True)   # ou ascending=False
```

**Renomear / criar colunas**
```python
df.rename(columns={'old': 'new'})

df['log2FC'] = df['c1'] - df['c2']
df['sig'] = df['padj'] < 0.05
```

**Apply**
```python
df['gene'].apply(função)
```

**Strings**
```python
df['coluna'].str.strip()
df['coluna'].str.lower()
df['coluna'].str.split(';')
df['coluna'].str.contains('x')
df['coluna'].str.replace('x', 'y')
```

**Crosstab**
```python
pd.crosstab(df['Amostra'], df['Drug'])
#          Drug1  Drug2 ...
# Amostra1   freq   freq
# Amostra2   freq   freq
# equivalente a: df.groupby([...]).size().unstack()

pd.crosstab(df['A'], df['B'], normalize='index')
# margins=True   # adiciona totais de linha/coluna
```

**Rank**
```python
df.groupby('Amostra')['LFQ'].rank()
```

**Pivot table**
```python
df.pivot_table(index='gene', columns='Amostra', values='LFQ')
# gene  Am  LFQ            gene  V1   V2
# A     V1  100     ->     A     100  120
# A     V2  120            B     80   NaN
# B     V1  80
```

**Indexação — `.loc` vs `.iloc`**
```python
df.loc[linha, coluna]      # usa rótulos (nomes)
df.loc[:, 'coluna']
df.loc[df['coluna'] == 'a']

df.iloc[linha, coluna]     # usa índices (posição)
df.iloc[:, 0:3]
```

**Contas por linha**
```python
df[colunas].função(axis=1)

# soma
df['soma'] = df[colunas].sum(axis=1)

# média
df[colunas].mean(axis=1)
```

**Filtrar coluna por padrão (nome)**
```python
df.filter(like='LFQ', axis=1).columns
```

**Explode**
```python
df = df.explode('drug_class')
# x drug_class     ->   x drug
# bla [1,2]             bla 1
#                        bla 2
```

**Groupby**
```python
df.groupby(by='Amostra').size()                    # contagem
df.groupby('Amostra')['LFQ'].mean()
df.groupby(['Amostra', 'drug']).size()
#          A  d1  3
#             d2  4
#          B  d1  3
#             d2  5
```

**Reset index** — transforma o índice do groupby em coluna
```python
r = (df.groupby('Amostra')
       .size()
       .reset_index(name='count'))
# Amostra  count
# A        3
# B        4
```

**Pivot (via groupby + unstack)**
```python
(df.groupby(['Amostra', 'DC'])
   .size()
   .unstack(fill_value=0))   # preenche combinações faltantes com 0
```

**Merge**
```python
df = pd.merge(df1, df2, on='gene')
# how='left'

pd.concat([df1, df2])
```

**Drop**
```python
df.drop_duplicates()
df.drop_duplicates(subset='gene')   # duplicata considerando só essa coluna
```

**NaN**
```python
df.isna().sum()
df.dropna()
df.fillna(0)
```

**Filtrar top genes**
```python
df.nlargest(20, 'LFQ')
df.nsmallest(20, 'LFQ')
```

**Salvar**
```python
df.to_csv('nome.csv', index=False)
# sep='\t'  para tsv
```

**Dict comprehension**
```python
dict_novo = {key: value for (key, value) in iteration}
```

### Complemento (o que não estava no caderno)

Filtros extras:
```python
# ~ nega a condição
df[~df['gene'].isin(['blaKPC'])]   # tudo MENOS blaKPC

# where / mask: mantém o shape, troca valor em vez de filtrar linha
df['LFQ'].where(df['LFQ'] > 0, other=0)   # negativo vira 0
```

Tipos e conversão:
```python
df['coluna'] = df['coluna'].astype(float)
df['coluna'] = pd.to_numeric(df['coluna'], errors='coerce')  # vira NaN se não converter
df['data'] = pd.to_datetime(df['data'])
```

Apply na linha inteira e map:
```python
# apply na linha inteira (axis=1) -> quando a função precisa de mais de uma coluna
df['risco'] = df.apply(lambda row: 'alto' if row['LFQ'] > 100 and row['p'] < 0.05 else 'baixo', axis=1)

# map: troca valores usando um dicionário (bom pra renomear categorias)
mapa = {'V1': 'Variante1', 'V2': 'Variante2'}
df['Amostra_nome'] = df['Amostra'].map(mapa)
```

Groupby avançado:
```python
# Múltiplas agregações de uma vez
df.groupby('Amostra')['LFQ'].agg(['mean', 'std', 'count'])

# Agregações diferentes por coluna
df.groupby('Amostra').agg({'LFQ': 'mean', 'p': 'min'})

# Nomeando a coluna resultante direto
df.groupby('Amostra').agg(LFQ_medio=('LFQ', 'mean'))

# transform: devolve o resultado no mesmo shape do df original (bom pra normalizar por grupo)
df['LFQ_norm'] = df['LFQ'] / df.groupby('Amostra')['LFQ'].transform('sum')
```

Merge com mais detalhe:
```python
# how: 'inner' (padrão, só o que casa), 'left', 'right', 'outer' (tudo)
pd.merge(df1, df2, on='gene', how='left')

# Quando o nome da coluna-chave é diferente nos dois dfs
pd.merge(df1, df2, left_on='gene_id', right_on='ARO', how='left')

# indicator=True: mostra de onde veio cada linha (útil pra debugar merge)
pd.merge(df1, df2, on='gene', how='outer', indicator=True)
```

Outros formatos de salvamento:
```python
df.to_excel('saida.xlsx', index=False)
df.to_parquet('saida.parquet')     # mais rápido e leve pra tabelas grandes (usado no ARGOS)
pd.read_parquet('saida.parquet')
```
