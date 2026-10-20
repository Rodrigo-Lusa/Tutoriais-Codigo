## Script de checagem rápida (exemplo real de uso)
Padrão pra checar se todos os arquivos esperados de um pipeline existem:
```bash
#!/bin/bash
# uso: bash checar_outputs.sh lista_samples.txt pasta_resultados/

LISTA=$1
PASTA=$2

while read -r sample; do
    ARQ="${PASTA}/${sample}_rgi.txt"
    if [ -s "$ARQ" ]; then
        echo "OK    - $sample"
    else
        echo "FALTA - $sample ($ARQ)"
    fi
done < "$LISTA"
```

## Extras úteis pra análise rápida de arquivos
```bash
# Contar quantas sequências tem num fasta
grep -c "^>" arquivo.fasta

# Contar linhas de um fastq (÷4 = número de reads)
zcat amostra.fastq.gz | wc -l

# Ver só o cabeçalho de um csv/tsv grande
head -1 tabela.csv

# Checar tamanho de vários arquivos de uma vez
du -sh *.fastq.gz

# Loop + condicional pra mover arquivos vazios pra revisão
mkdir -p revisar
for f in *.txt; do
    if [ ! -s "$f" ]; then
        mv "$f" revisar/
    fi
done

# set -e: para o script se algum comando falhar (bom pra scripts de pipeline)
set -e
set -u   # erro se usar variável não definida
```
