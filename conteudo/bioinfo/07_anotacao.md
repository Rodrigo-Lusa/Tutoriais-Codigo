## 🏷️ Anotação

### Prokka
[github.com/tseemann/prokka](https://github.com/tseemann/prokka)
Anotação rápida de genomas bacterianos completos (isolados) — gene calling +
anotação funcional numa etapa só.

- **Script:** `scripts/annotation/run_prokka.sh`
- **Versão testada:** v1.14.6
- **Uso:** `./run_prokka.sh [genomes_dir] [annotations_dir]`
- **Skip:** pula genoma já anotado (detecta pelo `.faa` de saída); remove e
  re-roda se encontrar uma pasta de output parcial (rodada anterior
  interrompida).
- **Correção:** a versão anterior deste script tinha um typo nas mensagens de
  log (`"nvalid FASTA"`, `"artial output"` — faltava a primeira letra); corrigido.

**Estrutura gerada:**
```text
prokka_annotations/
└── <genoma>/
    ├── <genoma>.faa      # usado no RGI
    ├── <genoma>.ffn
    ├── <genoma>.gff
    ├── <genoma>.gbk
    └── ...
```

### Prodigal
[github.com/hyattpd/Prodigal](https://github.com/hyattpd/Prodigal)
Gene calling standalone (mais rápido que Prokka, sem anotação funcional).
Usado em dois contextos diferentes, com uma flag que MUDA entre eles:

- **MAGs** (`scripts/annotation/run_prodigal_rgi.sh`) — usa `-p meta`
  (genoma fragmentado/comunidade mista, cada contig pode ser de espécie diferente)
- **Isolados** (`scripts/annotation/run_prodigal_rgi_isolates.sh`) — **sem**
  `-p meta` (modo padrão/single: assume genoma completo de uma espécie só,
  gene calling mais preciso pra esse caso)

### Pipeline de anotação de isolados (Prodigal + RGI + geNomad + ABRicate)

Pensado pra rodar em escala (ex: ~7000 genomas bacterianos) — cada etapa
paraleliza **entre genomas** via GNU parallel (não dentro de 1 genoma, que é
rápido demais pra valer a pena), e pula genoma/etapa já processado.

- **Orquestrador:** `scripts/annotation/run_annotation_pipeline.sh` — chama as
  3 etapas abaixo em sequência.
  ```bash
  ./run_annotation_pipeline.sh genomes/ /caminho/genomad_db 64
  ```

**1. Prodigal (isolado) + RGI CARD**
- **Script:** `scripts/annotation/run_prodigal_rgi_isolates.sh`
- **Uso:** `./run_prodigal_rgi_isolates.sh genomes/ 64` (genomes_dir, JOBS)
- **Paralelização:** 64 genomas simultâneos (GNU parallel), RGI com 1 thread
  cada (`-n 1`) — evita oversubscription, usa os 64 núcleos disponíveis 1:1.
- **Skip:** por genoma, granular (Prodigal e RGI checados separadamente).
- **Copia automaticamente** os `_rgi.txt` pra `resistome/` — pronto pro
  `argos update`.

**Estrutura gerada:**
```text
prodigal_out/<genoma>.faa/.ffn/.gff
rgi_out/<genoma>/<genoma>_rgi.txt
resistome/<genoma>_rgi.txt          # entrada do ARGOS
logs/tool_versions.txt
logs/prodigal_rgi_isolates.joblog   # log do GNU parallel (coluna Exitval)
```

**2. geNomad** (padrão, sem flags especiais)
[github.com/apcamargo/genomad](https://github.com/apcamargo/genomad)
Classifica cada contig como cromossomo / plasmídeo / vírus — usado pra
cruzar mobilidade genética com risco de AMR (quantos genes Rank I estão em
contigs de plasmídeo, por exemplo).

- **Script:** `scripts/annotation/run_genomad.sh`
- **Uso:** `./run_genomad.sh <input_dir> <output_dir> <db_path> [JOBS] [THREADS_PER_JOB]`
  (default: 16 jobs × 4 threads = 64 núcleos)
- **Skip:** pula genoma cuja pasta de output já não está vazia.
- **Nota:** o comando do geNomad em si não mudou (`end-to-end --cleanup`,
  padrão) — só passou a rodar vários genomas em paralelo via GNU parallel em
  vez de um loop sequencial.

**Estrutura gerada (por genoma):**
```text
output_dir/<genoma>/
├── <genoma>_summary/
│   ├── <genoma>_virus_summary.tsv
│   ├── <genoma>_plasmid_summary.tsv
│   └── ...
└── <genoma>_find_proviruses/
```

**3. ABRicate** (bancos não-resistência)
[github.com/tseemann/abricate](https://github.com/tseemann/abricate)
Screening rápido contra bancos de referência via BLAST. Rodamos só os bancos
**não** relacionados a resistência (resistência já é coberta com mais
profundidade pelo RGI/CARD):

| Incluídos | Excluídos (redundantes com RGI/CARD) |
|---|---|
| `vfdb` (virulência) | `card` |
| `plasmidfinder` (replicons) | `resfinder` |
| `ecoh` (antígenos O/H de *E. coli*) | `argannot` |
| `ecoli_vf` (virulência de *E. coli*) | `megares`, `ncbi` |

- **Script:** `scripts/amr/run_abricate.sh`
- **Versão testada:** v1.0.1
- **Uso:** `./run_abricate.sh genomes/ 64` (genomes_dir, JOBS)
- **Skip:** por combinação genoma+banco.
- **Gera resumo consolidado** (`abricate --summary`) por banco no final.

**Estrutura gerada:**
```text
abricate_out/
├── <genoma>/
│   ├── <genoma>_vfdb.tab
│   ├── <genoma>_plasmidfinder.tab
│   ├── <genoma>_ecoh.tab
│   └── <genoma>_ecoli_vf.tab
├── summary_vfdb.tab
├── summary_plasmidfinder.tab
├── summary_ecoh.tab
└── summary_ecoli_vf.tab
```

### arg_ranker *(fica de fora do pipeline automatizado por enquanto)*
[github.com/xiaole99/ARG_ranker](https://github.com/xiaole99/ARG_ranker) *(confirme a URL certa do seu fork/versão)*
Rankeia ARGs por risco (Rank I-IV) usando um banco próprio.

- **Funcionamento real da ferramenta** (importante — é diferente dos outros):
  ela **não roda genoma por genoma**. Você aponta pra uma pasta inteira, ela
  **gera um script** com uma linha por genoma, e você roda esse script:
  ```bash
  arg_ranker -i $INPUT                    # gera arg_ranking/script_output/arg_ranker.sh
  sh arg_ranking/script_output/arg_ranker.sh   # <- aqui é sequencial, 1 thread por genoma
  ```
- **Gargalo:** a segunda linha roda cada genoma um de cada vez. Em escala
  (~7000 genomas) isso é o problema.
- **Ideia de correção (ainda não implementada, ver com calma):** não editar
  nenhuma linha do script gerado — só trocar como ele é *executado*, de
  `sh script.sh` (sequencial) pra `parallel -j 64 :::: script.sh` (roda as
  linhas em paralelo). Sem risco de mexer no que o arg_ranker gerou.
