## conda — um ambiente por ferramenta

> Seus envs: `argos`, `rgi`, `genomad`, `ncbi_datasets`, `fastp`, `bbtools_env`,
> `blobtools`, `interpro_env`, `plots_env`, `resistomex`. Ferramenta de bioinfo
> costuma brigar por versão de dependência — por isso um env cada.

### Dia a dia
```bash
conda env list                          # lista os envs
conda activate rgi                      # entra
conda deactivate                        # sai
conda create -n genomad -c conda-forge -c bioconda genomad   # cria já instalando
conda install -n rgi -c bioconda rgi=6.0.3                   # instala versão exata
conda list | grep pandas                # versão instalada de um pacote
conda env export -n argos > argos.yml   # salva o ambiente (reprodutibilidade)
conda env create -f argos.yml           # recria a partir do yml
conda env remove -n env_velho
```

### Ativar conda DENTRO de um script ⭐
```bash
# `conda activate` não funciona em script sem carregar o conda.sh antes
CONDA_SH="$(conda info --base)/etc/profile.d/conda.sh"
source "$CONDA_SH"
conda activate ncbi_datasets
bash baixar_lote.sh "$LISTA" "$DESTINO"
conda activate rgi
bash run_prodigal_rgi_isolates.sh "$DESTINO" 64

# Alternativa sem ativar: conda run
conda run -n genomad genomad --version
```
