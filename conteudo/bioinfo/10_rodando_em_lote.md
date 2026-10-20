## Rodando em lote (todas as amostras)

Todo script de `scripts/*/run_*.sh` aceita uma amostra por chamada. Pra rodar
numa lista de amostras com resumo de falhas no final, use `run_batch` de
`lib/checks.sh`:
```bash
#!/usr/bin/env bash
source scripts/lib/checks.sh

run_batch scripts/binning/run_metabat2.sh \
    Mangrove/VAN1/ \
    Mangrove/VAN2/ \
    atlantic_florest/MAF1/
```
Como cada script já pula amostras/etapas já processadas, rodar esse loop de
novo depois de uma falha no meio do caminho é seguro — só as amostras que
faltaram (ou falharam) vão de fato rodar de novo.
