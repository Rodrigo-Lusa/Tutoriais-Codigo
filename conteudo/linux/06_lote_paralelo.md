## Lote e paralelo (while read, GNU parallel, xargs)

> Como você roda escala (~7000 genomas): **paralelo ENTRE genomas** com GNU
> parallel, cada job com poucas threads. Regra: `JOBS × THREADS_POR_JOB ≈ nº de núcleos`.

### `while read` — uma linha por vez
```bash
while read -r acc; do
    [ -z "$acc" ] && continue                     # pula linha vazia
    ls "$DESTINO"/"${acc}"* &> /dev/null || echo "faltando: $acc"
done < lista_accessions.txt
```

### GNU parallel ⭐
```bash
# Básico: {} = cada item
parallel -j 8 'gzip {}' ::: *.fastq              # ::: lista na própria linha
parallel -j 8 'echo {}' :::: lista.txt          # :::: lê os itens de um arquivo

# Substituições
#   {}   arquivo completo    pasta/GCF_1.fna
#   {.}  sem extensão        pasta/GCF_1
#   {/}  só o nome           GCF_1.fna
#   {/.} nome sem extensão   GCF_1
#   {//} só a pasta          pasta

# Padrão dos seus scripts: função bash + export -f + joblog
process_genome() { prodigal -i "$1" -a "out/$(basename "$1" .fna).faa" -q; }
export -f process_genome log log_error is_valid_fasta   # funções viram visíveis pro parallel
export PRODIGAL_DIR RGI_THREADS                          # variáveis também

parallel -j "$JOBS" --joblog logs/prodigal.joblog \
    'process_genome {} > logs/{/.}.log 2>&1' ::: "${genomas[@]}"

# Resumo pelo joblog (coluna 7 = código de saída)
n_total=$(($(wc -l < logs/prodigal.joblog) - 1))
n_falha=$(awk 'NR>1 && $7!=0' logs/prodigal.joblog | wc -l)
awk 'NR>1 && $7!=0 {print $NF}' logs/prodigal.joblog     # quais falharam

# Re-rodar só o que falhou
parallel --retry-failed --joblog logs/prodigal.joblog
```

### xargs — alternativa curta
```bash
find . -name "*.fastq" | xargs -P 4 -I{} gzip {}    # -P 4 jobs, -I{} marca o item
```

### `run_batch` (de `lib/checks.sh`) — sequencial com resumo
```bash
source scripts/lib/checks.sh
run_batch scripts/binning/run_metabat2.sh Mangrove/VAN1/ Mangrove/VAN2/
```

### Lote de lotes (o fluxo do `scripts/`)
```bash
python gerar_lotes.py metadata.csv 500 lotes/        # quebra accessions em lote_001.txt...
bash rodar_tudo.sh lotes/ /db/genomad_db 64 16 4     # um lote por vez: baixa -> RGI -> geNomad -> apaga .fna
```

### Deixar rodando depois de fechar o terminal
```bash
nohup bash rodar_tudo.sh lotes/ db > rodar_tudo.log 2>&1 &   # & manda pro fundo
tail -f rodar_tudo.log
# ou: tmux new -s lote  (sai com Ctrl-b d, volta com tmux attach -t lote)
```
