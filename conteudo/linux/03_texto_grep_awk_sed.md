## Texto: grep, cut, awk, sed, sort/uniq

> Os quatro que mais aparecem nos seus scripts: `awk` pra filtrar/selecionar
> coluna (hmmsearch, joblog do parallel), `sed` pra limpar nome/sequência,
> `head`/`wc` pra conferir output, `cut`/`rev` pra extrair pedaço do caminho.

### grep — achar linhas
```bash
grep "blaKPC" resistome.tsv          # linhas que contêm
grep -v "^#" arquivo.out             # -v inverte: tudo que NÃO começa com #
grep -c ">" genoma.fasta             # -c conta (aqui: nº de sequências)
grep -i "kpc" resistome.tsv          # -i ignora maiúscula/minúscula
grep -w "KPC-2" resistome.tsv        # -w palavra inteira (não casa KPC-21)
grep -E "KPC|NDM|OXA-48" res.tsv     # -E regex estendida (| = ou)
grep -l "Perfect" */*_rgi.txt        # -l só o NOME dos arquivos que casam
grep -rn "skip_if_done" scripts/     # -r recursivo, -n número da linha
```

### cut — colunas por delimitador
```bash
cut -f1,3 tabela.tsv                 # colunas 1 e 3 (tsv é o padrão: -d$'\t')
cut -d',' -f2 metadata.csv           # csv
cut -d'/' -f2 <<< "atlantic_florest/MAF3/resistome"   # MAF3
```

### awk — o canivete suíço de tabela ⭐
```bash
# Anatomia: awk 'CONDIÇÃO {AÇÃO}' arquivo
#   $1, $2... = colunas | $NF = última coluna | NR = nº da linha | NF = nº de colunas

awk '!/^#/' hits.out                          # remove comentários (do run_magscot.sh)
awk '!/^#/{print $1"\t"$3"\t"$5}' hits.out     # remove comentário + pega colunas 1,3,5
awk 'NR>1 && $7!=0 {print $NF}' x.joblog       # joblog do parallel: comandos que falharam
awk 'NR>1 && $7!=0' x.joblog | wc -l           # ...e quantos falharam
awk -F'\t' '$3 > 90' blast.tsv                 # -F define o separador; filtra identidade > 90
awk -F',' '{print NF; exit}' metadata.csv      # quantas colunas tem o csv

# Somar/agrupar
awk -F'\t' '{s += $2} END {print s}' tabela.tsv                    # soma coluna 2
awk -F'\t' '{n[$1]++} END {for (k in n) print k, n[k]}' t.tsv      # contagem por valor da col 1
```

### sed — substituir/editar texto
```bash
sed 's/antigo/novo/' arq             # troca a 1ª ocorrência de cada linha
sed 's/antigo/novo/g' arq            # g = todas as ocorrências
sed -i 's/antigo/novo/g' arq         # -i edita o arquivo no lugar (cuidado!)
sed 's/\*$//' proteinas.faa          # remove * do fim da linha (stop codon do Prodigal)
sed 's/_1.*//' <<< "SRR123_1.fastq"  # SRR123 -> nome da amostra a partir do R1
sed -n '10,20p' arq                  # imprime só as linhas 10 a 20
sed '/^$/d' arq                      # apaga linhas vazias
```

### sort / uniq / wc / head / tail
```bash
sort -k2,2nr tabela.tsv              # ordena pela coluna 2, numérico, decrescente
cut -f1 res.tsv | sort | uniq -c | sort -rn   # ranking de frequência (padrão clássico)
sort -u lista.txt                    # únicos
wc -l < lista.txt                    # nº de linhas, sem o nome do arquivo
head -n1 tabela.tsv | tr '\t' '\n' | cat -n    # lista o nome das colunas numeradas
tail -f logs/genomad.log             # acompanha um log enquanto o job roda
```

### Pipes e redirecionamento
```bash
cmd > saida.txt          # sobrescreve
cmd >> saida.txt         # acrescenta
cmd 2> erro.log          # só stderr
cmd > out.log 2>&1       # stdout + stderr no mesmo arquivo (usado no parallel)
cmd &> /dev/null         # descarta tudo (ex: command -v parallel &> /dev/null)
cmd | tee log.txt        # mostra na tela E salva
```
