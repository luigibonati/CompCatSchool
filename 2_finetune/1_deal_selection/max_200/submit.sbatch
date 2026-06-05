#!/bin/bash
#SBATCH --account=IscrB_ProAmmo
#SBATCH --partition=boost_usr_prod  # partition to be used
#SBATCH --time 24:00:00             # format: HH:MM:SS
#SBATCH --nodes=1                   # node
#SBATCH --ntasks-per-node=1         # tasks out of 32
#SBATCH --cpus-per-task=32
###SBATCH --qos=boost_qos_dbg
###SBATCH --time 00:30:00             # format: HH:MM:SS
############################

#source env
module load intel-oneapi-tbb
module load intel-oneapi-compilers
module load intel-oneapi-mpi
module load openblas/0.3.21--gcc--11.3.0
module load intel-oneapi-mkl

mamba activate /leonardo/pub/userexternal/lbonati1/envs/deal

# Program folder
deal -c deal.yaml --max 200 -f traj.xyz

