"""
Cheat sheet de Linux, Python e bioinformática.

O conteúdo mora em conteudo/<aba>/NN_tema.md (legível também no GitHub); este
app só lê os arquivos e monta as abas. O catálogo "Meus scripts" é gerado a
partir do cabeçalho de cada arquivo em bioinformatics/scripts/.

Rodar: streamlit run app.py
"""

import ast
import re
from pathlib import Path

import streamlit as st

RAIZ = Path(__file__).resolve().parent
CONTEUDO = RAIZ / "conteudo"
SCRIPTS = RAIZ / "bioinformatics" / "scripts"

ABAS = {
    "linux": "🐧 Linux",
    "python": "🐍 Python",
    "bioinfo": "🧬 Bioinfo",
}
PASTAS_SCRIPTS = {
    "download": "📥 Download",
    "qc": "🧹 QC",
    "assembly": "🧬 Montagem",
    "mapping": "🗺️ Mapeamento",
    "binning": "🗂️ Binning",
    "bin_refinement": "🧩 Refinamento",
    "annotation": "🏷️ Anotação",
    "amr": "💊 AMR",
    "viz": "📊 Visualização",
    "batch": "📦 Lote",
    "lib": "🔧 lib",
}


# ------------------------------------------------------------------ leitura
@st.cache_data
def ler_aba(pasta: str) -> list[tuple[str, str]]:
    """(rótulo curto, markdown) de cada conteudo/<pasta>/*.md, na ordem do nome."""
    paginas = []
    for arq in sorted((CONTEUDO / pasta).glob("*.md")):
        texto = arq.read_text(encoding="utf-8")
        paginas.append((rotulo(texto, arq.stem), texto))
    return paginas


def rotulo(texto: str, padrao: str) -> str:
    """Primeiro '## Título' encurtado: corta em ' — ', ' (' ou ':'."""
    m = re.search(r"^##\s+(.+)$", texto, re.MULTILINE)
    titulo = m.group(1) if m else padrao
    titulo = re.split(r" — | \(|:", titulo)[0]
    return titulo.replace("`", "").strip()


def secoes(texto: str) -> list[str]:
    """Quebra um markdown nos '###' (pra busca mostrar só o trecho que interessa)."""
    partes = re.split(r"(?m)^(?=### )", texto)
    return [p.strip() for p in partes if p.strip()]


@st.cache_data
def catalogo_scripts() -> dict[str, list[dict]]:
    """Pasta -> lista de {nome, caminho, descricao, uso, codigo} dos scripts."""
    catalogo = {}
    ordem = list(PASTAS_SCRIPTS)  # ordem do pipeline; pasta nova não listada vai pro fim
    pastas = sorted((p for p in SCRIPTS.iterdir() if p.is_dir()),
                    key=lambda p: (ordem.index(p.name) if p.name in ordem else len(ordem), p.name))
    for pasta in pastas:
        itens = []
        for arq in sorted(pasta.iterdir()):
            if arq.suffix not in (".sh", ".py"):
                continue
            codigo = arq.read_text(encoding="utf-8", errors="ignore")
            cabecalho = cabecalho_py(codigo) if arq.suffix == ".py" else cabecalho_sh(codigo)
            itens.append({
                "nome": arq.name,
                "caminho": arq.relative_to(RAIZ).as_posix(),
                "descricao": cabecalho,
                "uso": linha_de_uso(cabecalho),
                "codigo": codigo,
                "linguagem": "python" if arq.suffix == ".py" else "bash",
            })
        if itens:
            catalogo[pasta.name] = itens
    return catalogo


def cabecalho_sh(codigo: str) -> str:
    """Bloco de comentários do topo do script (sem shebang e sem as linhas de ====)."""
    linhas = []
    for linha in codigo.splitlines()[1:]:
        if not linha.startswith("#"):
            break
        linha = linha.lstrip("#")
        if set(linha.strip()) <= {"=", "-"} and linha.strip():
            continue
        linhas.append(linha[1:] if linha.startswith(" ") else linha)
    return "\n".join(linhas).strip()


def cabecalho_py(codigo: str) -> str:
    try:
        return (ast.get_docstring(ast.parse(codigo)) or "").strip()
    except SyntaxError:
        return ""


def linha_de_uso(cabecalho: str) -> str:
    """Pega o(s) exemplo(s) depois de 'Uso:'."""
    m = re.search(r"Uso:?\s*\n?((?:.*\S.*\n?){1,3})", cabecalho, re.IGNORECASE)
    if not m:
        return ""
    linhas = [l.strip() for l in m.group(1).splitlines() if l.strip()]
    return "\n".join(l for l in linhas if not l.startswith("(")) or ""


# ------------------------------------------------------------------ páginas
def mostrar_aba(pasta: str) -> None:
    paginas = ler_aba(pasta)
    for sub, (_, texto) in zip(st.tabs([r for r, _ in paginas]), paginas):
        with sub:
            st.markdown(texto)


def mostrar_scripts() -> None:
    st.markdown(
        "Gerado a partir do cabeçalho de cada arquivo em `bioinformatics/scripts/`. "
        "Ferramenta, parâmetros e estrutura de saída estão na aba **🧬 Bioinfo**."
    )
    catalogo = catalogo_scripts()
    nomes = [PASTAS_SCRIPTS.get(p, p) for p in catalogo]
    for sub, itens in zip(st.tabs(nomes), catalogo.values()):
        with sub:
            for item in itens:
                st.markdown(f"#### `{item['nome']}`")
                st.caption(item["caminho"])
                if item["uso"]:
                    st.code(item["uso"], language="bash")
                with st.expander("Descrição e código"):
                    if item["descricao"]:
                        st.text(item["descricao"])
                    st.code(item["codigo"], language=item["linguagem"], line_numbers=True)


def mostrar_busca(termo: str) -> None:
    termo_low = termo.lower()
    achados = 0
    fontes = [(ABAS[p], ler_aba(p)) for p in ABAS] + [("⭐", [("Mais usados", (CONTEUDO / "mais_usados.md").read_text())])]
    for nome_aba, paginas in fontes:
        for rot, texto in paginas:
            for trecho in secoes(texto):
                if termo_low in trecho.lower():
                    achados += 1
                    with st.expander(f"{nome_aba} › {rot} › {trecho.splitlines()[0].lstrip('# ')}", expanded=achados <= 3):
                        st.markdown(trecho)
    for itens in catalogo_scripts().values():
        for item in itens:
            if termo_low in (item["nome"] + item["descricao"]).lower():
                achados += 1
                with st.expander(f"📜 Script › {item['nome']}"):
                    st.caption(item["caminho"])
                    st.text(item["descricao"])
    if not achados:
        st.info(f"Nada encontrado para “{termo}”.")
    else:
        st.caption(f"{achados} trecho(s) com “{termo}”.")


# ------------------------------------------------------------------ app
st.set_page_config(page_title="Cheat Sheet — Lusa", page_icon="📚", layout="wide")

with st.sidebar:
    st.title("📚 Cheat Sheet")
    st.caption("Linux, Python e bioinformática — consultar aqui antes de perguntar pra IA.")
    termo = st.text_input("🔎 Buscar em tudo", placeholder="groupby, parallel, awk, @classmethod...")
    st.divider()
    st.markdown((CONTEUDO / "links.md").read_text(encoding="utf-8"))

if termo.strip():
    st.header(f"🔎 “{termo.strip()}”")
    mostrar_busca(termo.strip())
else:
    nomes = ["⭐ Mais usados", *ABAS.values(), "📜 Meus scripts"]
    tabs = st.tabs(nomes)
    with tabs[0]:
        st.markdown((CONTEUDO / "mais_usados.md").read_text(encoding="utf-8"))
    for tab, pasta in zip(tabs[1:], ABAS):
        with tab:
            mostrar_aba(pasta)
    with tabs[-1]:
        mostrar_scripts()
