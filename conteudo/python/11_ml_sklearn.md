## Machine learning com scikit-learn

> Do `ml_isolados_brasileiros`: `train_test_split` → `Pipeline`
> (`ColumnTransformer` + `StandardScaler`/`OneHotEncoder` + modelo) →
> `GridSearchCV` com `StratifiedKFold` → métricas. Clustering: KMeans/DBSCAN/
> Agglomerative avaliados por silhouette, Calinski-Harabasz e Davies-Bouldin.

### Fluxo completo de classificação ⭐
```python
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold, cross_val_predict
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, balanced_accuracy_score, ConfusionMatrixDisplay

X = df.drop(columns=["Risco", "Species"])
y = df["Risco"]
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

num = X.select_dtypes("number").columns
cat = X.select_dtypes(exclude="number").columns
pre = ColumnTransformer([
    ("num", StandardScaler(), num),
    ("cat", OneHotEncoder(handle_unknown="ignore"), cat),
])
pipe = Pipeline([("pre", pre), ("modelo", RandomForestClassifier(random_state=42))])

grid = GridSearchCV(
    pipe,
    param_grid={"modelo__n_estimators": [100, 300], "modelo__max_depth": [None, 5, 10]},  # <etapa>__<param>
    cv=StratifiedKFold(n_splits=5, shuffle=True, random_state=42),
    scoring="balanced_accuracy",      # bom pra classe desbalanceada
    n_jobs=-1,
)
grid.fit(X_tr, y_tr)
grid.best_params_, grid.best_score_

y_pred = grid.best_estimator_.predict(X_te)
print(classification_report(y_te, y_pred))
ConfusionMatrixDisplay.from_predictions(y_te, y_pred, normalize="true")

# Sem conjunto de teste: predição out-of-fold (cada amostra prevista por um modelo que não a viu)
y_oof = cross_val_predict(grid.best_estimator_, X, y, cv=5)
```

### Modelos que você usa (troca só a última etapa do Pipeline)
| Sigla | Classe | Hiperparâmetros típicos |
|---|---|---|
| knn | `KNeighborsClassifier` | `n_neighbors`, `weights` |
| svm | `SVC` / `SVR` | `C`, `kernel`, `gamma` |
| rf | `RandomForestClassifier` | `n_estimators`, `max_depth` |
| gbm | `GradientBoostingClassifier` | `learning_rate`, `n_estimators` |
| nb | `GaussianNB` | `var_smoothing` |
| — | `NearestCentroid`, `BayesianRidge` | |
| nn | `tensorflow.keras` (via wrapper) | camadas, `optimizer`, `activation` |

### Métricas
```python
from sklearn.metrics import (accuracy_score, balanced_accuracy_score, precision_score,
                             recall_score, f1_score, r2_score, mean_squared_error, mean_absolute_error)
f1_score(y_te, y_pred, average="macro")              # macro = média simples entre classes
r2_score(y_true, y_pred); mean_squared_error(y_true, y_pred) ** 0.5   # RMSE (regressão)
```

### Seleção de features
```python
from sklearn.feature_selection import VarianceThreshold, SelectKBest, f_classif
VarianceThreshold(0.01).fit_transform(X)         # tira coluna quase constante (gene presente em ~todos)
sel = SelectKBest(f_classif, k=20).fit(X, y); X.columns[sel.get_support()]
```

### Clustering
```python
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score
from sklearn.decomposition import PCA

Xs = StandardScaler().fit_transform(df[FEATURES])          # SEMPRE escalar antes
for k in range(2, 9):
    lab = KMeans(n_clusters=k, n_init=10, random_state=42).fit_predict(Xs)
    print(k, silhouette_score(Xs, lab),                   # maior = melhor (-1..1)
             calinski_harabasz_score(Xs, lab),            # maior = melhor
             davies_bouldin_score(Xs, lab))               # MENOR = melhor

DBSCAN(eps=0.5, min_samples=5).fit_predict(Xs)            # -1 = ruído
AgglomerativeClustering(n_clusters=4, linkage="ward").fit_predict(Xs)

pca = PCA(n_components=2).fit(Xs)
coords = pca.transform(Xs); pca.explained_variance_ratio_
```

### Salvar e carregar modelo
```python
import joblib
joblib.dump(grid.best_estimator_, "modelos/rf.joblib")
modelo = joblib.load("modelos/rf.joblib"); modelo.predict(X_novo[X.columns])   # mesmas colunas, mesma ordem
```

### Armadilhas
- `fit` do scaler **só no treino** — dentro do `Pipeline` isso já é garantido.
- `stratify=y` no split e `StratifiedKFold` na CV quando a classe é desbalanceada.
- Genomas da mesma espécie/surto no treino e no teste vazam informação → considere `GroupKFold`.
