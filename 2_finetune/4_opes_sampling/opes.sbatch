#!/bin/bash
#SBATCH --account=IscrB_ProAmmo
#SBATCH --time 24:00:00             # format: HH:MM:SS
#SBATCH --nodes=1                   # node
#SBATCH --ntasks-per-node=1         # tasks out of 32
#SBATCH --gres=gpu:1                # gpus per node out of 4
#SBATCH --cpus-per-task=8
#SBATCH -p boost_usr_prod
##SBATCH --qos=boost_qos_dbg
############################
 
# source env
source ~/.bashrc
 
ENV_PATH="/leonardo_scratch/fast/IscrB_ProAmmo/envs/compcatschool" 
mamba activate "$ENV_PATH"

module purge
module load profile/base
module load cuda/12.6                                                               
module load openmpi/4.1.6--gcc--12.2.0-cuda-12.2
module load fftw/3.3.10--openmpi--4.1.6--gcc--12.2.0-spack0.22
module load gcc/12.2.0
module load gsl/2.7.1--gcc--12.2.0-spack0.22
module load intel-oneapi-mkl/2024.0.0--intel-oneapi-mpi--2021.12.1
. /leonardo_scratch/fast/IscrB_ProAmmo/plumed-2.10.0/sourceme.sh

# pass them from environment variables via --export=TEMP="$TEMP",BIAS="$BIAS",BARRIER="$BARRIER" 
TEMP=700
BIAS="OPES_METAD_EXPLORE"
BARRIER=0.8

python ../1_opes/opes.py --temperature $TEMP --bias $BIAS --barrier $BARRIER --franken best_ckpt.pt --outdir "test/" --system '../../0_system/init_config.xyz'
