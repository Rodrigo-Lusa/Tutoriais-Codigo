## 🧬 Montagem

### metaSPAdes
[github.com/ablab/spades](https://github.com/ablab/spades)
Montador escolhido após comparação com MEGAHIT (ver `teste_montadores.md` do
mestrado — metaSPAdes deu contigs com maior contiguidade). Modo `metaSPAdes`
do SPAdes.

- **Script:** `scripts/assembly/run_metaspades.sh`
- **Versão testada:** v3.13.1 [metaSPAdes mode]
- **Uso:** `./run_metaspades.sh <sample_dir>/`
- **Skip:** pula a amostra se `scaffolds.fasta` já existir.
- **Entrada esperada:** `<sample_dir>/reads/*1_paired*`, `*2_paired*`, `*singleton*`

**Estrutura gerada:**
```text
<sample_dir>/
└── metaspades_out/
    ├── scaffolds.fasta      # usado nas etapas seguintes
    ├── contigs.fasta
    └── ...
```
