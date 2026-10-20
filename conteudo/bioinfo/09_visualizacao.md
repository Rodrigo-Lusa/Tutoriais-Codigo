## 📊 Visualização

### Blobtools
[github.com/DRL/blobtools](https://github.com/DRL/blobtools)
Gera "blobplots" (GC% × cobertura, colorido por taxonomia ou por bin) — bom
pra checar contaminação/heterogeneidade numa montagem de metagenoma.

- **Script:** `scripts/viz/run_blobtools.sh` — consolida BLASTn + DIAMOND +
  `blobtools create/view/plot` num pipeline só, com skip por etapa.
- **Script auxiliar:** `scripts/viz/bin2catcolour.py` — gera o TSV de cor por
  bin (`--catcolour`), a partir dos `.fna` dos bins na pasta atual.
- **Versões testadas:** Blobtools 1.1.1, BLASTn 2.17.0+, DIAMOND 2.1.24.178
- **Uso:**
  ```bash
  python bin2catcolour.py                     # gera blobplot_bin_colour.tsv
  ./run_blobtools.sh scaffolds.fasta alignment.sorted.bam meu_blobplot blobplot_bin_colour.tsv
  ```

**Estrutura gerada:**
```text
meu_blobplot.blast.out
meu_blobplot.diamond.out
meu_blobplot.blobDB.json
meu_blobplot.<taxlevel>.p8.span.100.blobplot.bam0.png   # o gráfico
```
