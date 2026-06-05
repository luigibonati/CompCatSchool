#!/bin/bash
#SBATCH --account=IscrB_ProAmmo
##SBATCH --time 24:00:00            # format: HH:MM:SS
#SBATCH --nodes=1                   # node
#SBATCH --ntasks-per-node=4         # tasks out of 32
#SBATCH --gres=gpu:4                # gpus per node out of 4
#SBATCH --cpus-per-task=8
#SBATCH -p boost_usr_prod
#SBATCH --qos=boost_qos_dbg 
#SBATCH --export=NONE
#SBATCH --job-name='Franken'
############################
 

ENV_PATH="/leonardo/pub/userexternal/lbonati1/envs/franken" 
mamba activate "$ENV_PATH"

export OMP_NUM_THREADS=${SLURM_CPUS_PER_TASK}

BACKBONE="mace_mh/0" 
OUT_DIR="autotune/${BACKBONE}"

torchrun --standalone --nnodes=1 --nproc-per-node=${SLURM_NTASKS_PER_NODE} ${ENV_PATH}/bin/franken.autotune \
    --train-path train.xyz --val-path val.xyz \
    --l2-penalty="(-10, -5, 6, log)" \
    --force-weight="[0.01,0.1,0.5,0.9,0.99,0.999]" \
    --jac-chunk-size "auto" \
    --run-dir "${OUT_DIR}" \
    --backbone=mace --mace.path-or-id "${BACKBONE}" \
    --metrics energy_MAE forces_MAE forces_MAE_species \
    --best-model-selection energy_MAE forces_MAE_species_average \
    --rf=gaussian --gaussian.num-rf "8192" --gaussian.length-scale="[1,5,10,20,25,30]"

#franken.wrap_mace_lammps --model_path ./${OUT_DIR}/*/best_ckpt.pt
