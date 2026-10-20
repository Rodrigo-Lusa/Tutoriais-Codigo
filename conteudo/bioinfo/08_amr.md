## 💊 AMR (Antimicrobial Resistance)

> `scripts/amr/run_abricate.sh` (virulência/plasmídeos, bancos não-resistência)
> também mora aqui na pasta, mas está documentado dentro do pipeline de
> anotação de isolados (aba 🏷️ Anotação) porque roda em conjunto com Prodigal+RGI+geNomad.

### RGI + CARD
[github.com/arpcard/rgi](https://github.com/arpcard/rgi)
Anota genes de resistência a antimicrobianos comparando proteínas preditas
contra o banco CARD/WildCARD.

- **Script (isolados, a partir de `.faa` do Prokka):** `scripts/amr/run_rgi.sh`
- **Script (MAGs, Prodigal + RGI num pipeline só):** `scripts/annotation/run_prodigal_rgi.sh`
- **Versões testadas:** RGI v6.0.5, CARD 4.0.1, WildCARD 3.2.7
- **Skip:** ambos pulam amostra já processada (detecta pelo `_rgi.txt` de saída).
- **Correção:** `run_rgi.sh` documentava modo `--local` no comentário mas o
  comando não tinha a flag — adicionada, pra bater com o que está
  documentado.

**Estrutura gerada (`run_rgi.sh`, por isolado):**
```text
<isolado>/
├── <isolado>.faa
└── <isolado>_rgi.txt      # tabela de genes de resistência
```

**Estrutura gerada (`run_prodigal_rgi.sh`, por MAG):**
```text
prodigal_out/<mag>.faa/.ffn/.gff/.gbk
prodigal_clean/<mag>.faa        # sem '*' de stop codon (exigido pelo RGI)
rgi_out/<mag>/<mag>_rgi.txt
resistome/<mag>_rgi.txt         # cópia final -- entrada do ARGOS
logs/tool_versions.txt
```

### RGI-BWT (KMA)
[docs (rgi_bwt)](https://github.com/arpcard/rgi/blob/master/docs/rgi_bwt.rst)
Alternativa ao Prodigal+RGI: mapeia as **reads** direto contra CARD/WildCARD
via KMA, sem precisar montar/anotar genes antes.

- **Script:** `scripts/amr/run_rgi_bwt.sh`
- **Uso:** `./run_rgi_bwt.sh read_1.fastq read_2.fastq outdir/ [nome_amostra]`
- **Skip:** pula amostra já mapeada.

**Estrutura gerada:**
```text
outdir/
└── <amostra>_kma_mapping_out.gene_mapping_data.txt   # usado nas análises seguintes
```

### group_resistome.py
Não é uma ferramenta externa — é o script que agrega todas as tabelas
`_rgi.txt` de uma pasta num único CSV (`Assembly` extraído do nome do
arquivo), pronto pra virar entrada do ARGOS.

- **Script:** `scripts/amr/group_resistome.py`
- **Uso:** `python group_resistome.py rgi_txt_files/ -o resistoma_total.csv`
- **Correção:** antes existia duplicado (uma cópia por projeto, cada uma com
  o nome do CSV de saída hardcoded). Agora `-o` é parâmetro — um script só
  serve qualquer projeto.
