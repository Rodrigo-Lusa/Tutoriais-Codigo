## 🗂️ Binning

Os 3 binners rodam **em paralelo, independentemente**, sobre a mesma montagem
+ mapeamento — o refinamento (MAGScoT) depois decide qual bin de qual
ferramenta manter.

### MetaBAT2
[bitbucket.org/berkeleylab/metabat](https://bitbucket.org/berkeleylab/metabat/src/master/)
Binning por cobertura + composição de tetranucleotídeos. Instalado via Docker
no seu setup.

- **Script:** `scripts/binning/run_metabat2.sh`
- **Versão testada:** 2:2.17.89-gc869c52-dirty
- **Uso:** `./run_metabat2.sh <sample_dir>/`
- **Skip:** pula se a pasta de bins já existir.

**Estrutura gerada:**
```text
<sample_dir>/
├── metaspades_out/scaffolds.fasta.gz
└── scaffolds.fasta.gz.metabat-bins<N>/
    ├── bin.1.fa
    ├── bin.2.fa
    └── ...
```

### MetaDecoder
[github.com/liu-congcong/MetaDecoder](https://github.com/liu-congcong/MetaDecoder)
Binning usando modelo de linguagem (embedding) + cobertura.

- **Script:** `scripts/binning/run_metadecoder.sh`
- **Versão testada:** 1.2.2
- **Uso:** `./run_metadecoder.sh <sample_dir>/`
- **Skip:** pula se já existir `METADECODER.*.fasta`.

**Estrutura gerada:**
```text
<sample_dir>/
└── metadecoder_out/
    ├── METADECODER.COVERAGE
    ├── METADECODER.SEED
    ├── METADECODER.1.fasta      # bins finais
    ├── METADECODER.2.fasta
    └── ...
```

### COMEBin
[github.com/ziyewang/COMEBin](https://github.com/ziyewang/COMEBin/tree/master)
Binning por contrastive learning multi-view.

- **Script:** `scripts/binning/run_comebin.sh` **(wrapper novo)**
- **Uso:** `./run_comebin.sh <sample_dir>/`
- **Skip:** pula se já existirem bins em `comebin_out/comebin_res/comebin_res_bins/`.
- **Nota:** padronizei o nome da pasta de saída pra `comebin_out` (a
  documentação antiga usava `comebin_output`, mas o script de agregação
  espera `comebin_out`).

**Estrutura gerada:**
```text
<sample_dir>/
└── comebin_out/
    └── comebin_res/
        └── comebin_res_bins/
            ├── bin.1.fa
            └── ...
```
