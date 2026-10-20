## Scripts robustos (o padrão dos seus `run_*.sh`)

> Todo `run_*.sh` em `bioinformatics/scripts/` segue o mesmo esqueleto:
> modo estrito → carrega `lib/checks.sh` → valida argumentos → define
> variáveis com default → pula o que já foi feito → loga.

### Esqueleto completo ⭐
```bash
#!/usr/bin/env bash
# =============================================================================
# run_ferramenta.sh -- o que faz, em uma linha
# Uso: ./run_ferramenta.sh <input_dir> <output_dir> [THREADS]
# =============================================================================
set -euo pipefail
#   -e  para no primeiro erro
#   -u  erro se usar variável não definida (pega erro de digitação)
#   -o pipefail  um pipe falha se QUALQUER comando dele falhar
# Em script que usa GNU parallel use `set -uo pipefail` (sem -e): uma falha
# num genoma não pode matar o lote inteiro.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"   # pasta do script, de onde quer que rode
source "${SCRIPT_DIR}/../lib/checks.sh"                        # log, skip_if_done, run_batch...

if [ $# -lt 2 ]; then
    log_error "Uso: $0 INPUT_DIR OUTPUT_DIR [THREADS]"
    exit 1
fi

INPUT_DIR="$1"
OUTPUT_DIR="$2"
THREADS="${3:-8}"              # default 8 se não passar o 3º argumento

mkdir -p "$OUTPUT_DIR" logs

if ! command -v prodigal &> /dev/null; then
    log_error "prodigal não encontrado -- ativou o env certo?"
    exit 1
fi
```

### `lib/checks.sh` — funções que você reaproveita
| Função | O que faz |
|---|---|
| `log "msg"` / `log_warn` / `log_error` | mensagem colorida com timestamp (`log_error` vai pro stderr) |
| `is_valid_output arq` | existe e não está vazio (`[ -s arq ]`) |
| `is_valid_fasta arq` | não vazio e começa com `>` |
| `skip_if_done "desc" output cmd...` | se o output já existe, loga `[SKIP]`; senão roda o comando |
| `run_batch script am1 am2...` | roda o script pra cada amostra e no fim lista as que falharam |
| `log_tool_version "Nome" cmd --version` | grava a versão da ferramenta em `$VERSION_LOG` |

```bash
skip_if_done "Prodigal para $base" "$faa" \
    prodigal -i "$genome" -a "$faa" -d "$ffn" -o "$gff" -f gff -p meta -q

VERSION_LOG="logs/tool_versions.txt"; : > "$VERSION_LOG"   # `: >` zera o arquivo
log_tool_version "RGI" rgi main --version
```

### Substituição de comando e expansão de variável ⭐
```bash
n=$(wc -l < lista.txt)                 # $(...) guarda a saída de um comando
hoje=$(date '+%Y-%m-%d')

arq="genomas/GCF_000123.1_genomic.fna"
echo "$(basename "$arq")"              # GCF_000123.1_genomic.fna
echo "$(basename "$arq" .fna)"         # GCF_000123.1_genomic   (tira a extensão)
echo "$(dirname "$arq")"               # genomas

base="GCF_000123.1_genomic.fna"
echo "${base%.*}"        # GCF_000123.1_genomic   %  tira o MENOR sufixo que casa
echo "${base%%.*}"       # GCF_000123             %% tira o MAIOR sufixo
echo "${base#*_}"        # 000123.1_genomic.fna   #  tira o menor prefixo
echo "${amostra%/}"      # tira a barra final de "Mangrove/VAN1/"
echo "${VAR:-padrao}"    # usa "padrao" se VAR estiver vazia/indefinida
echo "${base/genomic/X}" # substitui a 1ª ocorrência
echo "${#base}"          # tamanho da string

echo $(( 16 * 4 ))       # aritmética: 64
```

### Funções, `local` e `return`
```bash
process_genome() {
    local genome="$1"                 # local: não vaza pra fora da função
    local base; base=$(basename "$genome" .fna)
    is_valid_fasta "$genome" || { log_warn "inválido: $genome"; return 1; }
    log "processando $base"
}
```

### Arquivos temporários e limpeza (`mktemp` + `trap`)
```bash
TMP_DIR=$(mktemp -d)                  # pasta temporária única (do baixar_lote.sh)
TMP_ZIP=$(mktemp --suffix=.zip)
trap 'rm -rf "$TMP_DIR" "$TMP_ZIP"' EXIT   # apaga no fim, mesmo se der erro
```

### Testes úteis no `if`
| Teste | Verdadeiro se |
|---|---|
| `-f arq` / `-d dir` | é arquivo / é pasta |
| `-s arq` | existe e não está vazio |
| `-z "$v"` / `-n "$v"` | string vazia / não vazia |
| `[[ $x == *.fna ]]` | casa padrão (só com `[[ ]]`) |
| `[[ $x =~ ^SRR[0-9]+$ ]]` | casa regex |
| `cmd1 && cmd2` / `cmd1 \|\| cmd2` | roda cmd2 se cmd1 deu certo / falhou |

### `shopt -s nullglob`
```bash
shopt -s nullglob                    # glob sem resultado vira lista vazia (e não o texto "*.fna")
genomas=("$INPUT_DIR"/*.fna "$INPUT_DIR"/*.fasta)
echo "${#genomas[@]} genomas"         # tamanho do array
```
