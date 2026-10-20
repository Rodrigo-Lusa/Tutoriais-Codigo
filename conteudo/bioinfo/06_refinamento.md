## 🧩 Refinamento de bins

### MAGScoT
[github.com/ikmb/MAGScoT](https://github.com/ikmb/MAGScoT)
Combina os bins dos 3 binners (score por marcadores single-copy TIGRFAM/Pfam)
e escolhe o melhor conjunto não-redundante de bins refinados.

- **Script principal:** `scripts/bin_refinement/run_magscot.sh` — pipeline completo:
  `Prodigal → HMMsearch (TIGRFAM + Pfam) → contigs_to_bin.tsv → MAGScoT.R → extract_mags.py`
- **Scripts auxiliares:**
  - `obtain_contigs_to_bin.py` — junta os bins de ComeBin/MetaDecoder/MetaBAT2
    num único TSV `BIN<TAB>CONTIG<TAB>BINNER`
  - `extract_mags.py` — extrai um `.fasta` por bin refinado
  - `make_unbinned.py` — extrai os contigs que **não** caíram em nenhum bin
    (viram um pseudo-bin, também entram na entrada do ARGOS)
- **Uso:** `./run_magscot.sh <sample_dir>/` (precisa de `MAGSCOT_DIR` apontando
  pro clone do repositório MAGScoT — default: pasta `MAGScoT/` no cwd)
- **Skip:** granular por etapa (Prodigal, HMMsearch, tsv, refinamento — cada
  um só roda se o output daquela etapa específica não existir). Isso
  substitui os dois scripts antigos (`run_magscot.sh` + `magscot_final.sh`,
  que eram quase o mesmo script duplicado).

**Estrutura gerada:**
```text
<sample_dir>/
├── magscot_out/
│   ├── <amostra>.prodigal.faa/.ffn
│   ├── <amostra>.hmm.tigr.hit.out / .hmm.pfam.hit.out
│   ├── <amostra>.hmm                        # combinado
│   ├── <amostra>.contigs_to_bin.tsv
│   ├── MAGScoT.refined.out
│   ├── MAGScoT.refined.contig_to_bin.out    # mapeamento final contig -> bin
│   └── MAGScoT.scores.out
└── refined_mags/
    ├── <amostra>_bin_1.fasta
    ├── <amostra>_bin_2.fasta
    └── ...
```
E, rodando `make_unbinned.py` sobre todas as amostras:
```text
unbinned_contigs/
├── <amostra1>_unbinned.fasta
├── <amostra2>_unbinned.fasta
└── ...
```

### CheckM2
[github.com/chklovski/CheckM2](https://github.com/chklovski/CheckM2)
QC de completude/contaminação de genomas e MAGs.

- **Sem wrapper** — comando único, rodado sobre todos os MAGs de uma vez:
  ```bash
  conda activate checkm2
  checkm2 predict --threads 30 --input MAGs/ --output-directory MAGs_checkm_results
  ```
- **Versão testada:** 1.1.0
- **Filtro usado no projeto:** Completeness ≥ 98%, Contamination < 5%, N50 ≥ 10.000

**Estrutura gerada:**
```text
MAGs_checkm_results/
├── quality_report.tsv     # Completeness, Contamination, N50 por MAG
└── diamond_output/
```
