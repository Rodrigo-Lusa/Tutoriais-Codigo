## Script básico (anatomia)
```bash
#!/bin/bash
# Shebang: diz ao sistema qual interpretador usar pra rodar o script

# Variáveis (sem espaço ao redor do =)
PASTA="resultados"
EXT=".fasta"

# Usando a variável -> $VAR ou ${VAR}
echo "Procurando arquivos $EXT em $PASTA"

# Argumentos de linha de comando
# $0 = nome do script, $1 = primeiro argumento, $2 = segundo, etc.
# $# = número de argumentos, $@ = todos os argumentos
echo "Script: $0"
echo "Primeiro argumento: $1"
echo "Total de argumentos: $#"

# Rodar: bash script.sh amostra1
```

Dar permissão de execução e rodar direto:
```bash
chmod +x script.sh
./script.sh amostra1
```

## if / else
```bash
#!/bin/bash
ARQUIVO=$1

# Sintaxe: espaço depois de [ e antes de ]  é obrigatório
if [ -f "$ARQUIVO" ]; then
    echo "É um arquivo"
elif [ -d "$ARQUIVO" ]; then
    echo "É um diretório"
else
    echo "Não existe: $ARQUIVO"
fi
```

Testes mais usados dentro de `[ ]`:
```bash
-f arquivo      # existe e é arquivo comum
-d pasta        # existe e é diretório
-e caminho      # existe (arquivo ou pasta)
-s arquivo      # existe e não está vazio (size > 0)
-r / -w / -x    # tem permissão de leitura / escrita / execução

# Comparação de strings
[ "$a" == "$b" ]     # igual
[ "$a" != "$b" ]     # diferente
[ -z "$a" ]           # string vazia
[ -n "$a" ]           # string não vazia

# Comparação numérica (NÃO usa == para números)
[ "$a" -eq "$b" ]    # igual
[ "$a" -ne "$b" ]    # diferente
[ "$a" -gt "$b" ]    # maior que
[ "$a" -lt "$b" ]    # menor que
[ "$a" -ge "$b" ]    # maior ou igual
[ "$a" -le "$b" ]    # menor ou igual

# Combinando condições
if [ -f "$ARQUIVO" ] && [ -s "$ARQUIVO" ]; then   # E
if [ -f "$ARQUIVO" ] || [ -d "$ARQUIVO" ]; then   # OU
```

## Loops (for / while) — pra checagem em massa
```bash
# For sobre arquivos (glob)
for f in *.fastq.gz; do
    echo "Processando $f"
done

# For sobre uma lista de amostras
AMOSTRAS="MAF1 MAF2 MAF3"
for amostra in $AMOSTRAS; do
    echo "Amostra: $amostra"
done

# While lendo linha por linha de um arquivo (ex: lista de samples)
while read -r linha; do
    echo "Sample: $linha"
done < lista_samples.txt
```
