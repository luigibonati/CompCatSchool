# School on Computational Catalysis

Tutorial material for the First International School on Computational Catalysis.

10-12 June 2026, Modena

Lecturers: Luigi Bonati, Massimo Bocus, and Daniela Polino.

This repository illustrates a molecular-dynamics workflow for heterogeneous
catalysis using the dissociation of N2 on Fe(111) as an example. It will features
machine learning potentials (universal models and fine-tuned), enhanced sampling 
calculations for both free energies and kinetics estimation, and analysis of active sites in dynamical
environments. The case study is inspired by the work on surface dynamics and 
N2 decomposition on Fe(111): <https://www.pnas.org/doi/10.1073/pnas.2313023120>.

## Repository Layout

```text
0_system/
  create_system.ipynb   Build system.

1_opes/
  opes.ipynb            Free energy estimation via OPES.

2_fine-tune/
  TODO

3_kinetics/
  TODO

4_active_sites/
```

## Requirements

- Python 3.12
- ase 3.28.0
- PyTorch 2.10
- mace 0.3.15
- PLUMED 2.10.0

### Local Installation

Create and activate a Python environment:

```bash
conda create -n compcatschool python=3.12 -y
conda activate compcatschool
```

Install PyTorch and MACE. The example below targets CUDA 12.6; adapt the wheel
index to the CUDA driver available on your machine.

```bash
pip install torch==2.10.0 --index-url https://download.pytorch.org/whl/cu126
pip install ase mace-torch==0.3.15
```

Download and compile PLUMED:

```bash
wget https://github.com/plumed/plumed2/releases/download/v2.10.0/plumed-2.10.0.tgz
tar xvf plumed-2.10.0.tgz
cd plumed-2.10.0
./configure --enable-modules=all
make -j16
. sourceme.sh
```

To load PLUMED automatically in future shells, add the generated `sourceme.sh`
line to your shell startup file:

```bash
echo ". $PWD/sourceme.sh" >> ~/.bashrc
```

Install the Python wrapper:

```bash
conda install -c conda-forge py-plumed -y
```

### HPC Installation (Cineca Leonardo)

```bash
conda create -n compcatschool python=3.12 -y
conda activate compcatschool
```

```bash
module load cuda/12.6
pip install torch==2.10.0 --index-url https://download.pytorch.org/whl/cu126
pip install ase mace-torch==0.3.15
```

```bash
module purge
module load profile/base
module load openmpi/4.1.6--gcc--12.2.0-cuda-12.2
module load fftw/3.3.10--openmpi--4.1.6--gcc--12.2.0-spack0.22
module load gcc/12.2.0
module load gsl/2.7.1--gcc--12.2.0-spack0.22
module load intel-oneapi-mkl/2024.0.0--intel-oneapi-mpi--2021.12.1

mpicompiler=$(which mpicxx)
./configure --enable-modules=all CXX=${mpicompiler}
make -j16
. sourceme.sh
echo ". $PWD/sourceme.sh" >> ~/.bashrc
```

```bash
conda install -c conda-forge py-plumed -y
```