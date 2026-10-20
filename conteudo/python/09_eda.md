## Análise Exploratória de Dados (EDA)

### Roteiro mínimo só com pandas/seaborn (sem instalar nada novo)
```python
df.shape                       # (linhas, colunas)
df.info()                      # tipos + quantos non-null por coluna
df.describe(include='all')     # estatísticas (numéricas e categóricas)
df.isna().sum().sort_values(ascending=False)   # onde estão os NaN
df.nunique()                   # cardinalidade de cada coluna (detecta ID vs categoria)

# Correlação entre variáveis numéricas
sns.heatmap(df.corr(numeric_only=True), cmap='coolwarm', annot=True, center=0)

# Distribuição de cada variável numérica de uma vez
df.hist(figsize=(12, 8), bins=30)

# Relação entre pares de variáveis, colorido por categoria
sns.pairplot(df, hue='tipo', palette='husl')

# Duplicatas
df.duplicated().sum()
```

### Bibliotecas que fazem o relatório automático
Quando quer um overview rápido sem escrever tudo isso na mão:

- **ydata-profiling** (antigo `pandas-profiling`) — o mais completo: gera um HTML
  com distribuição, correlação, valores faltantes, alertas de qualidade (colunas
  constantes, alta cardinalidade, correlação alta entre pares) pra cada coluna.
  ```python
  from ydata_profiling import ProfileReport
  profile = ProfileReport(df, title="EDA", minimal=False)
  profile.to_file("eda_report.html")
  ```
  `minimal=True` deixa mais rápido em datasets grandes (pula algumas correlações caras).

- **sweetviz** — parecido, mais rápido de gerar, bom pra comparar dois datasets lado
  a lado (ex: treino vs teste, ou clínico vs ambiental).
  ```python
  import sweetviz as sv
  report = sv.compare([df_clinico, "Clínico"], [df_ambiental, "Ambiental"])
  report.show_html("comparacao.html")
  ```

- **missingno** — visualização específica pra padrão de dados faltantes (matriz,
  barra, dendrograma de correlação entre ausências). Útil quando o NaN não é
  aleatório (ex: um gene só é reportado se passou de um threshold).
  ```python
  import missingno as msno
  msno.matrix(df)
  msno.heatmap(df)   # correlação entre "faltar" em uma coluna e faltar em outra
  ```

### Recomendação prática
Pra uma checagem rápida do dia a dia (ex: conferir uma tabela nova do RGI/CARD
antes de meter no pipeline): `df.info()` + `df.describe()` + `df.isna().sum()`
já resolve. Pra um relatório que vai ser revisado por outra pessoa (banca,
supervisor) ou quando o dataset é novo e desconhecido: vale rodar `ydata-profiling`
uma vez e olhar os alertas — ele aponta coisas que passariam despercebidas
(coluna quase toda igual, dois campos muito correlacionados, outlier extremo).
