## Streamlit — app de dados em Python puro

> Usado no `ml_isolados_brasileiros/app` e neste cheat sheet. O script roda
> de cima a baixo **a cada interação** — por isso cache é essencial.

### Rodar
```bash
streamlit run app.py                                        # http://localhost:8501
streamlit run main.py --server.port=8080 --server.address=0.0.0.0   # dentro do docker / servidor
```

### Blocos básicos
```python
import streamlit as st

st.set_page_config(page_title="Cheat Sheet", page_icon="📚", layout="wide")   # 1ª chamada do script
st.title("Título"); st.header("Seção"); st.subheader("Sub")
st.markdown("**negrito** e `código`")                    # unsafe_allow_html=True pra CSS/HTML
st.write(df)                                             # "faz o que for melhor" com qualquer objeto
st.dataframe(df, use_container_width=True, hide_index=True)
st.code("ls -lh", language="bash")                       # já vem com botão de copiar
st.metric("Genomas", 7012, delta="+500")
st.pyplot(fig)                                           # figura do matplotlib
st.divider()
```

### Layout
```python
aba1, aba2 = st.tabs(["Linux", "Python"])
with aba1:
    st.write("conteúdo da aba")

col1, col2 = st.columns([2, 1])                          # larguras relativas
col1.metric("Treino", len(df_train))

with st.expander("Ver código"):
    st.code(texto)

with st.sidebar:
    busca = st.text_input("Buscar")
```

### Entrada do usuário
```python
modelo = st.selectbox("Modelo", ["kmeans", "dbscan", "agglomerative"])
ks = st.multiselect("Features", df.columns)
k = st.slider("k", 2, 10, 4)
if st.button("Rodar"):
    ...
arquivo = st.file_uploader("CSV", type="csv")
```

### Cache ⭐
```python
@st.cache_data              # resultado serializável (DataFrame, dict...) — lê o CSV 1 vez só
def carregar(caminho):
    return pd.read_csv(caminho)

@st.cache_resource          # objeto "vivo" (modelo, conexão)
def modelo():
    return joblib.load("rf.joblib")

# Em método de classe: o 1º argumento vira _self (o _ diz pro cache ignorá-lo)
class Paginas:
    @st.cache_data
    def busca_dados(_self): ...
```

### Multipágina
```python
pg = st.navigation([st.Page(pagina_inicio, title="Início"), st.Page("paginas/ml.py", title="ML")])
pg.run()
```

### Estado entre interações
```python
if "contador" not in st.session_state:
    st.session_state.contador = 0
st.session_state.contador += 1
```
