## seqkit — manipular FASTA e FASTQ

### seqkit — flags principais
```bash
# Estatísticas gerais
seqkit stats file.fa

# Manipular o arquivo de forma geral
seqkit seq [flags]
-n, --name                  # only print names/sequence headers
-r, --reverse                # reverse sequence
-s, --seq                    # only print sequences
-g, --remove-gaps            # remove gap letters
-i, --only-id                # print IDs instead of full headers
-M, --max-len                # only print sequences <= max length (-1 = no limit)
-m, --min-len                # only print sequences >= min length (-1 = no limit)

seqkit seq -m 100 -M 1000    # sequências entre 100 (-m) e 1000 (-M) pb

# Subsequências por região/gtf/bed, incluindo flanking sequences
seqkit subseq [flags]
-u, --up-stream          # tamanho a montante
-d, --down-stream        # tamanho a jusante
-f, --only-flank         # retorna só a sequência flanqueadora
-r, --region             # por região. ex: 1:12 (12 primeiras bases) / -12:-1 (12 últimas) / 13:-1 (corta as 12 primeiras)

# Buscar sequências por ID/nome/sequência/motif
seqkit grep [flags]
-n, --by-name             # busca pelo nome completo, não só o ID
-s, --by-seq              # busca subsequência dentro da seq
-C, --count                # só imprime a contagem de matches (com -v, conta os que não deram match)
-i, --ignore-case          # ignora maiúsculas/minúsculas
-v, --invert-match         # inverte a busca
-m, --max-mismatch         # mismatch máximo ao buscar por sequência
-p, --pattern               # padrão de busca (aceita múltiplos valores)
-f, --pattern-file          # arquivo de padrões (um registro por linha)
-r, --use-regexp            # trata os padrões como regex

seqkit grep -p "contig_name" file.fa
seqkit grep -f list.txt file.fa
seqkit grep -n -f name.txt file.fa
```

### Comandos básicos (grep puro, sem seqkit)
```bash
# Contar quantas sequências existem em um FASTA
cat arquivo.fasta | grep ">" | wc -l
grep -c "^>" arquivo.fasta          # ^ indica início da linha

# Mostrar apenas os nomes das sequências
cat arquivo.fasta | grep ">" | cut -f1
grep "^>" arquivo.fasta | cut -c2-

# Contar quantas reads existem em um FASTQ
cat reads.fq | grep "@" | wc -l

# Listar apenas as sequências (sem os headers)
cat arquivo.fasta | grep -v ">"
grep -v "^>" arquivo.fasta

# Encontrar sequências que contêm um padrão exato (ex: ATG)
cat arquivo.fasta | grep -w "ATG"

# Contar o número total de bases (A, T, G ou C) em um FASTA
grep -v ">" arquivo.fasta | tr -d '\n' | wc -c

# Extrair reads de um FASTQ que contenham "N" na sequência
cat reads.fq | grep "N"
grep -A1 "^@" reads.fq | grep "N"     # -A1: mostra a linha encontrada + 1 linha depois ("after")

# Ordenar os headers de um FASTA em ordem alfabética
grep "^>" arquivo.fasta | sort

# Contar quantas sequências começam com "ATG"
grep -v ">" arquivo.fasta | grep "^ATG" | wc -l
```
