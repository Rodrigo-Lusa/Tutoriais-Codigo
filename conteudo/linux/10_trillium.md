## Trillium — cluster SciNet

> Large parallel cluster construído pela Lenovo Canada e hospedado pelo SciNet na
> University of Toronto.

Diretórios principais:
- `/home` – arquivos pessoais e configurações.
- `/scratch` – armazenamento temporário de alta velocidade pra dados de job.
- `/project` – armazenamento compartilhado pra times/colaborações.

```bash
# Entrar no sistema
ssh -i ~/.ssh/ssh_key lusaro@trillium.alliancecan.ca

# Copiar arquivos do sistema para o computador local
scp -i ~/.ssh/ssh_key lusaro@trillium.alliancecan.ca:/scratch/lusaro/arquivo .
    # -r se for pasta
```

Trillium usa o sistema de environment modules pra gerenciar compiladores, bibliotecas e
outros pacotes de software:
```bash
module load <module-name>  # carrega a versão padrão de um pacote
module purge                # descarrega todos os módulos carregados
module avail                 # lista módulos disponíveis pra carregar
module list                  # mostra os módulos carregados no momento
module spider                # busca módulos disponíveis e suas versões
```

Script básico pra submeter um job (SLURM):
```bash
#!/bin/sh
#SBATCH -J NOME_DO_JOB
#SBATCH --time=3:00:00
#SBATCH --ntasks-per-node=40
#SBATCH --nodes=1

cd $SLURM_SUBMIT_DIR

module load CCEnv nixpkgs/16.09

parallel -j $SLURM_TASKS_PER_NODE <<EOF #opcional. Apenas para scripts em paralelo

<commands>

EOF
```
Referência rápida de flags do SBATCH mais usadas:
```bash
-J NOME            # nome do job
--time=HH:MM:SS    # tempo máximo alocado
--nodes=N          # número de nós
--ntasks-per-node=N # tarefas/cores por nó
--mem=16G           # memória alocada
-o saida.out         # arquivo de saída (stdout)
-e erro.err           # arquivo de erro (stderr)
```
```bash
# Comandos de gestão de job
sbatch script.sh     # submete o job
squeue -u $USER       # ver seus jobs na fila
scancel <job_id>       # cancela um job
sacct -j <job_id>       # histórico/status de um job já rodado
```
