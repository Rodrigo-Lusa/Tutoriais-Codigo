## 📥 Download

### NCBI `datasets`
[github.com/ncbi/datasets](https://github.com/ncbi/datasets)
Ferramenta oficial do NCBI para baixar genomas/assemblies em lote a partir de accessions.

- **Script:** `scripts/download/download_genomes.py`
- **Versão testada:** 18.16.0
- **Uso:** `python3 download_genomes.py genome_ids.txt -o fasta_files`
- **Skip:** pula IDs cujo `.fna` já existe e não está vazio.

**Estrutura gerada:**
```text
fasta_files/
├── GCA_000793345.1.fna
├── GCA_000793346.2.fna
└── ...
```

### `sra-tools` (prefetch + fasterq-dump)
[github.com/ncbi/sra-tools](https://github.com/ncbi/sra-tools)
Baixa `.sra` de uma run pública e converte pra FASTQ.

- **Script:** `scripts/download/baixar_reads_sra.sh`
- **Versão testada:** 3.2.1
- **Uso:** `./baixar_reads_sra.sh runs.txt outdir/`
- **Skip:** pula runs cujo `.fastq.gz` já existe no outdir.

**Estrutura gerada:**
```text
outdir/
├── SRR18469381_1.fastq.gz
├── SRR18469381_2.fastq.gz
└── ...
```
