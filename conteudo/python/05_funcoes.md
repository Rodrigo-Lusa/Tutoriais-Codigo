## Funções — estruturando algo complexo em várias funções

> Ideia central: uma função = uma responsabilidade. Se você descreve o que a função
> faz e precisa usar "e" no meio da frase, provavelmente ela devia ser duas funções.

### Anatomia básica
```python
def calcular_media(valores: list[float]) -> float:
    """Calcula a média de uma lista de valores."""
    return sum(valores) / len(valores)

# type hints (valores: list[float], -> float) não são obrigatórios, mas ajudam
# a documentar o que a função espera e retorna sem precisar ler o corpo inteiro
```

### Argumentos: posicionais, default e keyword-only
```python
def plot_heatmap(df, drug_class=None, cmap='viridis', *, cluster=False):
    # df, drug_class: podem ser passados por posição ou nome
    # cmap='viridis': valor default, não precisa passar se não quiser mudar
    # * antes de cluster: tudo depois só pode ser passado por nome (cluster=True)
    #   -> útil quando a função tem muitos parâmetros e você quer forçar clareza
    #      na chamada (evita plot_heatmap(df, None, 'viridis', True) ilegível)
    ...

plot_heatmap(df, cluster=True)          # ok
# plot_heatmap(df, None, 'viridis', True)  # funcionaria, mas ilegível
```

### Quebrando um problema complexo em várias funções
Exemplo no espírito do que o `plot_heatmap` do ARGOS faz: uma função "pública" que
orquestra, e funções internas menores que cada uma resolve uma parte.

```python
def plot_heatmap(dataset, drug_class=None, cluster=False, **kwargs):
    """Função pública: valida entrada, decide o caminho e delega."""
    matrix = _prepare_matrix(dataset, drug_class)

    if cluster:
        return _clustered_heatmap(matrix, **kwargs)
    else:
        return _render_heatmap(matrix, **kwargs)

def _prepare_matrix(dataset, drug_class):
    """Só prepara os dados: filtra e pivota. Não sabe nada de plot."""
    df = dataset.full_resistoma
    if drug_class is not None:
        df = df[df['drug_class'] == drug_class]
    return df.pivot_table(index='gene', columns='Amostra', values='count', fill_value=0)

def _render_heatmap(matrix, **kwargs):
    """Só sabe desenhar um heatmap simples. Não sabe de onde veio a matrix."""
    ...

def _clustered_heatmap(matrix, **kwargs):
    """Só sabe calcular distância (Jaccard/Bray-Curtis) e clusterizar."""
    ...
```

Por que separar assim:
- `_prepare_matrix` pode ser testada sozinha, sem precisar gerar nenhum gráfico.
- Se um bug aparece só no modo `cluster=True`, você sabe exatamente onde olhar.
- Funções com `_` na frente (convenção, não regra do Python) sinalizam "uso interno,
  não é pra ser chamada de fora do módulo".
- `**kwargs`: junta argumentos extras num dicionário e repassa pra frente sem
  precisar listar cada um — útil quando a função de baixo nível tem parâmetros
  de estilo (cor, tamanho da figura, etc.) que a de cima só quer repassar.

### Regra prática pra decidir quando quebrar em mais funções
```python
# Sinais de que já passou do ponto de quebrar:
# - função tem mais de ~30-40 linhas
# - você usa comentários tipo "### agora fazemos X" pra separar blocos dentro dela
#   -> cada bloco comentado é candidato a virar uma função
# - você repete o mesmo trecho de código em dois lugares diferentes
# - pra testar uma parte pequena, você precisa rodar a função inteira
```

### Docstrings e erro explícito (bom hábito pra funções reutilizáveis)
```python
def load_rgi_output(path: str) -> pd.DataFrame:
    """
    Lê o output do RGI (CARD) e retorna um DataFrame padronizado.

    Parameters
    ----------
    path : str
        Caminho pro arquivo .txt de saída do RGI.

    Returns
    -------
    pd.DataFrame
        Tabela com colunas renomeadas e tipos ajustados.
    """
    if not Path(path).exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {path}")

    df = pd.read_csv(path, sep='\t')
    return df
```
