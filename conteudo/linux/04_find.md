## find — cheat sheet para bioinformática

### Sintaxe geral
```bash
find [onde_procurar] [testes] [ações]
```
Pense sempre nessa ordem — `find ONDE TESTES AÇÕES`:
```bash
find . -type f -name "*.fastq.gz" -print
```
- `.` → procurar a partir daqui
- `-type f` → apenas arquivos
- `-name "*.txt"` → arquivos terminados em `.txt`

### Procurar por nome
```bash
find . -name "*.txt"          # todos os .txt
find . -iname "*.txt"         # ignorando maiúsculas/minúsculas
find . -name "*.tsv"
```

### Procurar por caminho completo
Quando você precisa de partes do caminho, não só do nome do arquivo:
```bash
find . -path "*/results/*.txt"                    # tudo dentro de uma pasta "results"
find . -path "*/final_resistome.tsv"               # exemplo real
```
Resultado (ex: em um projeto com várias amostras):
```text
./atlantic_florest/MAF3/resistome/07_final/final_resistome.tsv
./atlantic_florest/MAF1/resistome/07_final/final_resistome.tsv
./atlantic_florest/MAF2/resistome/07_final/final_resistome.tsv
```

### Apenas arquivos / apenas diretórios
```bash
find . -type f
find . -type d
```

### Contagem
```bash
find . -type f | wc -l                        # quantos arquivos existem
find . -name "*.tsv" | wc -l                    # quantos .tsv existem
find atlantic_florest -name "*.fa" | wc -l      # exemplo real
```

### Tempo de modificação
```bash
find . -mtime 0     # modificados nas últimas 24h
find . -mtime -7    # modificados nos últimos 7 dias
find . -mtime +30   # modificados há mais de 30 dias
```

### Arquivos vazios e permissões
```bash
find . -empty          # arquivos vazios
find . -executable      # arquivos executáveis
find . -writable        # arquivos graváveis
```

### Copiar arquivos
```bash
find . -name "*.txt" -exec cp {} backup/ \;          # um por vez
find . -name "*.txt" -exec cp -t backup {} +          # forma mais eficiente (menos processos cp)
```

### Renomear arquivos em massa
Adicionar prefixo:
```bash
find backup/ -name "*.tsv" \
-exec bash -c '
mv "$1" "$(dirname "$1")/OLD_$(basename "$1")"
' _ {} \;
# backup/final_resistome.tsv -> backup/OLD_final_resistome.tsv
```
Adicionar sufixo:
```bash
find . -name "*.txt" \
-exec bash -c '
mv "$1" "${1%.txt}_BACKUP.txt"
' _ {} \;
# arquivo.txt -> arquivo_BACKUP.txt
```
Trocar extensão:
```bash
find . -name "*.txt" \
-exec bash -c '
mv "$1" "${1%.txt}.csv"
' _ {} \;
```

### Operadores lógicos
```bash
find . -type f -name "*.txt"              # AND implícito
find . -type f -a -name "*.txt"           # AND explícito (equivalente)
find . \( -name "*.txt" -o -name "*.csv" \)   # OR
find . ! -name "*.txt"                     # NOT
```

### `-printf` — formatando a saída
```bash
%p    # caminho completo
%f    # apenas o nome do arquivo
%h    # diretório pai
%P    # remove o "./" inicial
```
```bash
find . -path "*/final_resistome.tsv" -printf "%P\n"
# atlantic_florest/MAF3/resistome/07_final/final_resistome.tsv
# atlantic_florest/MAF1/resistome/07_final/final_resistome.tsv
# atlantic_florest/MAF2/resistome/07_final/final_resistome.tsv
```

### Extraindo campos do caminho (cut / rev / awk)
```bash
# Primeiro campo
find . -path "*/final_resistome.tsv" -print0 | tr '\0' '\n' | cut -d/ -f1
# atlantic_florest

# Segundo campo
find . -path "*/final_resistome.tsv" -printf "%P\n" | cut -d/ -f2
# MAF3 / MAF1 / MAF2

# Dois primeiros campos
find . -path "*/final_resistome.tsv" -printf "%P\n" | cut -d/ -f-2
# atlantic_florest/MAF3 ...
```
`cut` não conta de trás pra frente — pra isso, `rev` (inverte a string, corta, inverte de volta):
```bash
# Último campo
find . -path "*/final_resistome.tsv" -printf "%P\n" | rev | cut -d/ -f1 | rev
# final_resistome.tsv

# Penúltimo campo
... | rev | cut -d/ -f2 | rev
# 07_final
```
Método melhor pra contar de trás pra frente — `awk` com `$NF` (last field):
```bash
awk -F/ '{print $NF}'        # último campo
awk -F/ '{print $(NF-1)}'    # penúltimo
awk -F/ '{print $(NF-2)}'    # terceiro a partir do fim
awk -F/ '{print $(NF-3)}'    # quarto a partir do fim

# Exemplo: extrair o nome da amostra do caminho
find . -path "*/final_resistome.tsv" -printf "%P\n" | awk -F/ '{print $(NF-3)}'
# MAF3 / MAF1 / MAF2
```

### Resumo mental

| Quero              | Comando                   |
| ------------------ | -------------------------- |
| Nome do arquivo    | `-name`                     |
| Caminho completo   | `-path`                     |
| Apenas arquivos    | `-type f`                   |
| Apenas diretórios  | `-type d`                   |
| Tamanho            | `-size`                     |
| Tempo              | `-mtime`                    |
| Profundidade       | `-maxdepth`                 |
| Executar comando   | `-exec`                     |
| Imprimir caminho   | `-print`                    |
| Imprimir formatado | `-printf`                   |
| Remover `./`       | `%P`                        |
| Último campo       | `awk -F/ '{print $NF}'`     |
| Penúltimo campo    | `awk -F/ '{print $(NF-1)}'` |
| Contar resultados  | `wc -l`                     |
| Operador AND       | `-a`                        |
| Operador OR        | `-o`                        |
| Operador NOT       | `!`                         |
