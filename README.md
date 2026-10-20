# Tutoriais
Author: Rodrigo Lusa (lusarodrigo4@gmail.com)

> Compilado de referências rápidas de bash e Python (pandas, numpy, matplotlib/seaborn,
> funções, classes, comprehensions, typer, scikit-learn, scipy, Streamlit) e dos guias de
> infraestrutura (find, seqkit, conda, Docker, Trillium) e ferramentas de bioinformática.
> Objetivo: consultar aqui antes de perguntar pra IA.

## Como usar

- **No navegador (com busca):** `streamlit run app.py` (env `argos`: `conda activate argos`)
- **No GitHub:** os links abaixo. Cada tema é um arquivo em [`conteudo/`](conteudo/).

- ⭐ [O que você mais usa](conteudo/mais_usados.md)

## 🐧 Linux / Bash

- [Script básico (anatomia)](conteudo/linux/01_script_basico.md)
- [Script de checagem rápida (exemplo real de uso)](conteudo/linux/02_checagem_arquivos.md)
- [Texto: grep, cut, awk, sed, sort/uniq](conteudo/linux/03_texto_grep_awk_sed.md)
- [find — cheat sheet para bioinformática](conteudo/linux/04_find.md)
- [Scripts robustos (o padrão dos seus run_*.sh)](conteudo/linux/05_scripts_robustos.md)
- [Lote e paralelo (while read, GNU parallel, xargs)](conteudo/linux/06_lote_paralelo.md)
- [seqkit — manipular FASTA e FASTQ](conteudo/linux/07_seqkit.md)
- [conda — um ambiente por ferramenta](conteudo/linux/08_conda.md)
- [Docker + Jupyter no servidor remoto](conteudo/linux/09_docker_jupyter.md)
- [Trillium — cluster SciNet](conteudo/linux/10_trillium.md)

## 🐍 Python

- [Python essenciais (argparse + pathlib, do zip)](conteudo/python/01_essenciais.md)
- [Typer — CLI (alternativa mais moderna ao argparse)](conteudo/python/02_typer.md)
- [Pandas](conteudo/python/03_pandas.md)
- [Numpy, Matplotlib e Seaborn](conteudo/python/04_graficos.md)
- [Funções — estruturando algo complexo em várias funções](conteudo/python/05_funcoes.md)
- [Dict e List Comprehension](conteudo/python/06_comprehension.md)
- [Classes — quando e como fazer](conteudo/python/07_classes.md)
- [Notebook + pasta src/ (o padrão dos seus projetos)](conteudo/python/08_notebook_src.md)
- [Análise Exploratória de Dados (EDA)](conteudo/python/09_eda.md)
- [Estatística com scipy](conteudo/python/10_estatistica.md)
- [Machine learning com scikit-learn](conteudo/python/11_ml_sklearn.md)
- [Streamlit — app de dados em Python puro](conteudo/python/12_streamlit.md)

## 🧬 Ferramentas de bioinformática

- [Visão geral — ferramentas de bioinformática](conteudo/bioinfo/00_visao_geral.md)
- [📥 Download](conteudo/bioinfo/01_download.md)
- [🧹 QC / Trimming](conteudo/bioinfo/02_qc.md)
- [🧬 Montagem](conteudo/bioinfo/03_montagem.md)
- [🗺️ Mapeamento](conteudo/bioinfo/04_mapeamento.md)
- [🗂️ Binning](conteudo/bioinfo/05_binning.md)
- [🧩 Refinamento de bins](conteudo/bioinfo/06_refinamento.md)
- [🏷️ Anotação](conteudo/bioinfo/07_anotacao.md)
- [💊 AMR (Antimicrobial Resistance)](conteudo/bioinfo/08_amr.md)
- [📊 Visualização](conteudo/bioinfo/09_visualizacao.md)
- [Rodando em lote (todas as amostras)](conteudo/bioinfo/10_rodando_em_lote.md)

## 📜 Scripts

Scripts prontos em [`bioinformatics/scripts/`](bioinformatics/scripts/), um por etapa do pipeline
(funções compartilhadas em [`lib/checks.sh`](bioinformatics/scripts/lib/checks.sh)). No app, a aba
**📜 Meus scripts** monta o catálogo automaticamente a partir do cabeçalho de cada arquivo.

## 🔗 Links úteis

- [Links](conteudo/links.md)
