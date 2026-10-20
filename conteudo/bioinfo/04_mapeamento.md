## 🗺️ Mapeamento

### Bowtie2 + Samtools
[github.com/BenLangmead/bowtie2](https://github.com/BenLangmead/bowtie2) ·
[github.com/samtools/samtools](https://github.com/samtools/samtools)
Mapeia as reads de volta contra o metagenoma montado — o BAM ordenado
resultante é a entrada de todos os binners.

- **Script:** `scripts/mapping/run_mapping.sh`
- **Versões testadas:** Bowtie2 v2.3.5.1, Samtools v1.17
- **Uso:** `./run_mapping.sh <sample_dir>/`
- **Skip:** pula a amostra se `mapping/alignment.sorted.bam(.bai)` já existir.
- **Nota:** consolida os antigos `make_bam_files.sh` e `pre_comebin.sh` (que
  faziam a mesma coisa) num script só, corrigindo um bug da versão antiga
  (variável `$SINGLE` indefinida em vez de `$singleton`).

**Estrutura gerada:**
```text
<sample_dir>/
└── mapping/
    ├── scaffold_index.*          # index do bowtie2
    ├── alignment.sorted.bam      # usado por MetaBAT2, MetaDecoder, COMEBin
    └── alignment.sorted.bam.bai
```
