## Requirements

* ase 
* mace
* franken
* PLUMED

## Install

Create environment with conda/mamba
```
conda create compcatschool python==3.12 -y
conda activate compcatschool
```

Install Pytorch and MACE
Note: Recent Pytorch versions assume CUDA>=13, here we are using CUDA=12.6, adapt based on the installed drivers
``` 
pip install torch==2.10.0 --index-url https://download.pytorch.org/whl/cu126
pip install ase mace-torch==0.3.15
```

Download and compile PLUMED
```
wget https://github.com/plumed/plumed2/releases/download/v2.10.0/plumed-2.10.0.tgz
tar xvf plumed-2.10.0.tgz
rm plumed-2.10.0.tgz
cd plumed-2.10.0/
./configure --enable-modules=all
make -j16 
. sourceme.sh
cp ~/.bashrc ~/.bashrc.backup
echo ". $PWD/sourceme.sh" >> ~/.bashrc
```

Install python wrappers for PLUMED
```
conda install -c conda-forge py-plumed -y
```

### Instructions for HPC installation (CINECA-Leonardo)

```
conda create --prefix /leonardo_scratch/fast/IscrB_ProAmmo/envs/compcatschool python==3.12 -y
conda activate /leonardo_scratch/fast/IscrB_ProAmmo/envs/compcatschool

module load cuda/12.6
pip install torch==2.10.0 --index-url https://download.pytorch.org/whl/cu126
pip install ase mace-torch==0.3.15

module purge
module load profile/base                                                               
module load openmpi/4.1.6--gcc--12.2.0-cuda-12.2
module load fftw/3.3.10--openmpi--4.1.6--gcc--12.2.0-spack0.22
module load gcc/12.2.0
module load gsl/2.7.1--gcc--12.2.0-spack0.22
module load intel-oneapi-mkl/2024.0.0--intel-oneapi-mpi--2021.12.1
mpicompiler=`which mpicxx`
./configure --enable-modules=all CXX=${mpicompiler}
make -j16 
. sourceme.sh
cp ~/.bashrc ~/.bashrc.backup
echo ". $PWD/sourceme.sh" >> ~/.bashrc

conda install -c conda-forge py-plumed -y
```