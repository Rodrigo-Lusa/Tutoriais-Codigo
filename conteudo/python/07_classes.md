## Classes — quando e como fazer

> **Função** = recebe dado, devolve resultado, não lembra de nada.
> **Classe** = junta **dado (atributos)** + **comportamento (métodos)** que
> trabalham sobre aquele dado. Vale a pena quando várias funções recebem
> sempre os mesmos argumentos (`df`, `target`, `features`...) — aí eles viram
> `self.df`, `self.target` e param de ser repassados toda hora.

### Anatomia mínima
```python
class Contador:                         # nome em CamelCase
    """O que a classe representa (docstring)."""

    especie_padrao = "E. coli"          # atributo de CLASSE: igual pra todos os objetos

    def __init__(self, genes: list[str]) -> None:   # roda ao criar o objeto
        self.genes = genes              # atributo de INSTÂNCIA: cada objeto tem o seu
        self.contagem_ = None           # sufixo _ = só preenchido depois de um método (estilo sklearn)

    def contar(self) -> dict:           # método: 1º argumento é sempre self (o próprio objeto)
        self.contagem_ = {g: self.genes.count(g) for g in set(self.genes)}
        return self.contagem_

c = Contador(["KPC-2", "NDM-1", "KPC-2"])   # cria (instancia) -> chama __init__
c.contar()                                 # {'KPC-2': 2, 'NDM-1': 1}
c.genes                                    # acessa atributo
```

### Vocabulário (tudo isso aparece no seu código)
| Coisa | Sintaxe | Pra quê | Onde você usa |
|---|---|---|---|
| atributo de instância | `self.x = ...` no `__init__` | estado de cada objeto | `Classifier.X`, `Clustering.features` |
| atributo "pós-fit" | `self.modelos_ = {}` | resultado que só existe depois de rodar | `Classifier.modelos_`, `melhores_parametros_` |
| método público | `def classify(self, ...)` | o que o usuário chama | `classify`, `regress`, `cross_validation` |
| método "interno" | `def _extrai(self)` | convenção: não chame de fora | `AmblerClassifier._extrai_stem` |
| método privado | `def __preprocessador(self)` | name mangling: vira `_Classe__preprocessador`, de fora nem aparece | `Classifier.__knn_classify`, `__avaliar` |
| `@staticmethod` | sem `self` | função utilitária que mora na classe | `AmblerClassifier._extrai_classe_ambler` |
| `@classmethod` | recebe `cls` | **construtor alternativo** (`from_...`) | `ArgosDataset.from_parquet` / `from_folder` |
| `@property` | `dataset.info` sem `()` | método que se comporta como atributo | `ArgosDataset.info` |
| `@dataclass` | campos anotados | gera `__init__`/`__repr__` sozinho | `ArgosDataset` |
| dunder | `__repr__`, `__call__`, `__getattr__` | integra com o Python (print, `obj()`, `obj.x`) | `_AttributeInfo`, `_InfoText` |
| herança | `class X(str)` | reaproveita outra classe | `_InfoText(str)` |

---

### Suas classes, por tipo de arquivo

| Tipo | Arquivo | Classe | Como iniciar |
|---|---|---|---|
| 📦 Container de dados | `argos/argos/core/dataset.py` | `ArgosDataset` | `ArgosDataset.from_parquet(pasta)` |
| 🤖 Modelo de ML (wrapper sklearn) | `ml_isolados_brasileiros/notebooks/src/classifier.py` | `Classifier` | `Classifier(df_train, target="Risco", df_test=df_test)` |
| 🤖 Modelo de ML | `.../notebooks/src/regression.py` | `Regression` | `Regression(df, target)` |
| 🤖 Modelo de ML | `.../notebooks/src/clustering.py` | `Clustering` | `Clustering(features, df, "kmeans")` |
| 📚 Catálogo / lookup | `.../notebooks/src/features_amr.py` | `AmblerClassifier` | `AmblerClassifier("data/raw/refgenes.tsv")` |
| 📚 Catálogo / lookup | `.../notebooks/src/features_risco.py` | `CatalogoBetaLactamase` | `CatalogoBetaLactamase(refgenes_path)` |
| 🖥️ Página Streamlit | `ml_isolados_brasileiros/app/src/paginas.py` | `Paginas` | `Paginas()` |
| 🖥️ Exibição de resultado | `.../app/src/modelos/{classifier,regression,clustering}.py` | `Classifier`, `Regression`, `Clustering` | recebem resultado já treinado |
| 🎨 Namespace de constantes | `bioinformatics/scripts/bin_refinement/obtain_contigs_to_bin.py` | `Cor` | não instancia: `Cor.VERDE` |
| 🔧 Auxiliar (dunders) | `argos/argos/core/dataset.py` | `_AttributeInfo`, `_InfoText` | uso interno do `.info` |

---

#### 📦 `ArgosDataset` — container de dados com `@dataclass`
```python
from argos.core.dataset import ArgosDataset

# Iniciar: NUNCA pelo construtor direto, sempre pelos @classmethod
dataset = ArgosDataset.from_parquet("../data/argos_project/parquet_data")             # projeto já salvo
dataset = ArgosDataset.from_parquet(pasta, samples=ids_finais)                        # só algumas amostras
dataset = ArgosDataset.from_folder(card_folder, metadata_path=..., exclude_loose=True) # a partir dos *_rgi.txt
```
| Atributos (dados) | Tipo |
|---|---|
| `resistome` | `pd.DataFrame` — 1 linha por hit |
| `metadata` | `pd.DataFrame` — amostra × atributo |
| `annotations` | `pd.DataFrame` — gene × drug_class/mechanism |
| `prevalence` | `pd.DataFrame` — prevalência da CARD |
| `genomad_genes`, `contigs` | `pd.DataFrame \| None` (só depois do geNomad) |
| `info` | `@property` — `dataset.info.resistome` explica a coluna; `dataset.info()` explica tudo |

| Métodos | Retorna |
|---|---|
| `card_resistome()` | dado bruto do RGI, carregado sob demanda (lazy) |
| `presence_absence()` / `count_matrix()` | matriz amostra × gene (recalculada a cada chamada) |
| `filter_samples(expr_ou_ids)` / `filter_genes(...)` | **novo** `ArgosDataset` filtrado |
| `to_parquet(pasta)` | salva em disco |
| `attach_contig_annotations()` | cruza resistoma com contigs do geNomad |

O padrão por trás:
```python
from dataclasses import dataclass, field

@dataclass
class ArgosDataset:
    resistome: pd.DataFrame                    # obrigatório
    metadata: pd.DataFrame
    contigs: pd.DataFrame | None = None        # opcional (com default vem DEPOIS dos obrigatórios)
    _parquet_dir: Path | None = field(default=None, repr=False, compare=False)  # interno, escondido do print

    @classmethod
    def from_parquet(cls, parquet_dir, samples=None) -> "ArgosDataset":
        ...                                    # lê os arquivos
        return cls(resistome=..., metadata=..., _parquet_dir=Path(parquet_dir))   # cls(...) == ArgosDataset(...)

    @property
    def info(self):
        return _AttributeInfo(_ATTRIBUTE_INFO)

    def filter_samples(self, ids) -> "ArgosDataset":
        return ArgosDataset(resistome=self.resistome[self.resistome.sample_id.isin(ids)], ...)  # não muda o original
```

#### 🤖 `Classifier` — wrapper de modelos sklearn
```python
from notebooks.src.classifier import Classifier   # (ou from src.classifier, conforme o sys.path)

clf = Classifier(df_train, target="cluster", df_test=df_test, descartar=["Species"],
                 scoring="balanced_accuracy")
metricas, y_pred = clf.classify("rf", n_splits=5)       # 'knn','svm','rf','gbm','nb','nn'
clf.modelos_["rf"].predict(df_novo[clf.X.columns])       # pipeline treinado, reutilizável
```
| Atributos | Quando existe |
|---|---|
| `X`, `y`, `X_test`, `y_test`, `target`, `scoring`, `descartar` | desde o `__init__` |
| `modelos_`, `melhores_parametros_` | depois de `classify()` |

| Método | Visível? | Papel |
|---|---|---|
| `classify(modelo, n_splits)` | público | escolhe o construtor, roda `GridSearchCV`, avalia |
| `__preprocessador()` | privado | monta o `ColumnTransformer`/`Pipeline` |
| `__knn_classify()`, `__rf_classify()`... | privado | devolvem `(estimator, param_grid)` de cada modelo |
| `__avaliar()`, `__metricas_pontuais()`, `__matrix_confusao()` | privado | métricas e gráficos |

O truque do **dicionário de métodos** (troca um `if/elif` gigante):
```python
def classify(self, modelo: str, n_splits: int = 5):
    construtores = {"knn": self.__knn_classify, "rf": self.__rf_classify, ...}   # método SEM () = referência
    if modelo not in construtores:
        raise ValueError(f"modelo {modelo!r} desconhecido -- use um de {list(construtores)}")
    estimator, param_grid = construtores[modelo]()                              # agora sim chama
```
`Regression` (`regress(modelo, n_splits, n_iter_search)`) e `Clustering`
(`cross_validation()`, `testar_modelo(best_param, df_test)`, `rotular_clusters()`)
seguem exatamente o mesmo molde: dados no `__init__`, um método público que
roda tudo, e os passos internos em `__metodos` privados.

#### 📚 `AmblerClassifier` / `CatalogoBetaLactamase` — catálogo carregado uma vez
Padrão "lê o arquivo de referência no `__init__`, depois responde perguntas rápidas":
```python
catalogo = CatalogoBetaLactamase("data/raw/refgenes.tsv")   # lê e monta self.funcao (dict) 1 vez
catalogo.classificar("OXA-23-like")                         # 'carbapenemase_serina' (lookup no dict)
resistome["funcao"] = resistome["gene_clean"].map(catalogo.classificar)   # aplica na coluna inteira

amb = AmblerClassifier("data/raw/refgenes.tsv")              # self.familias_por_classe
amb.classificar(nome_card)                              # "A", "B1", ... ou None
```
```python
class AmblerClassifier:
    def __init__(self, refgenes_path):
        ref = pd.read_csv(refgenes_path, sep="\t")
        ref["ambler_class"] = ref["product_name"].apply(self._extrai_classe_ambler)  # staticmethod via self
        self.familias_por_classe = ref.groupby("ambler_class")["familia"].apply(lambda s: sorted(s.unique()))

    @staticmethod
    def _extrai_classe_ambler(product_name):     # não usa self -> staticmethod
        m = re.search(r"class ([ABCD]) beta-lactamase", str(product_name), re.IGNORECASE)
        return m.group(1).upper() if m else None
```

#### 🖥️ `Paginas` — classe como agrupador de páginas Streamlit
```python
pagina = Paginas()
pagina.clustering()        # cada método público desenha uma página
pagina.metricas()
```
```python
class Paginas:
    @st.cache_data                    # cache do Streamlit: só lê o CSV na 1ª vez
    def busca_dados_cluster(_self):   # _self (com _) = "não use self pra montar a chave do cache"
        ...
```

#### 🎨 `Cor` — classe só pra agrupar constantes
```python
class Cor:
    VERDE = "\033[92m"
    RESET = "\033[0m"

print(f"{Cor.VERDE}ok{Cor.RESET}")   # não precisa instanciar
```

#### 🔧 `_AttributeInfo` — dunders na prática
```python
class _AttributeInfo:
    def __init__(self, texts: dict): self._texts = texts
    def __getattr__(self, name):     # obj.resistome -> procura no dict (só chamado se o atributo não existir)
        if name not in self._texts: raise AttributeError(name)
        return _InfoText(self._texts[name])
    def __call__(self):              # obj() -> imprime tudo
        for t in self._texts.values(): print(t)
    def __dir__(self):               # o que aparece no TAB do Jupyter
        return list(self._texts)

class _InfoText(str):                # herda de str
    def __repr__(self): return self  # no Jupyter, mostra o texto formatado em vez de 'texto\n...'
```

---

### Receita pra escrever uma classe nova
1. Escreva primeiro como você quer **usar** (`obj = X(df); obj.rodar()`), depois implemente.
2. `__init__` só guarda/valida os dados — nada pesado de cálculo, a não ser carregar um catálogo.
3. Um método público por "ação" do usuário; os passos dentro dele viram `__privados`.
4. Resultado de treino em atributo com `_` no fim (`modelos_`) e também devolvido no `return`.
5. Mais de um jeito de criar? `@classmethod from_xxx` em vez de `if` no `__init__`.
6. Só dados, sem comportamento? `@dataclass`.
7. Docstring com **Parâmetros / Atributos / Métodos / Exemplo** (como em `Classifier`).

### Inspecionar qualquer objeto
```python
type(obj)                  # classe
vars(obj)                  # dict dos atributos de instância
[m for m in dir(obj) if not m.startswith("_")]   # métodos/atributos públicos
help(Classifier)           # docstring + métodos
isinstance(obj, Classifier)
```
