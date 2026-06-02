# OPES Simulations

This folder contains the material for the OPES enhanced-sampling part of the
tutorial. The goal is to run biased molecular dynamics for N2 dissociation on
Fe(111), using a pretrained MACE-MP model for the forces and PLUMED/OPES for the
adaptive bias.

## Tutorial and Run Files

- `opes.ipynb`: notebook version of the workflow. It is meant to illustrate one
  selected OPES simulation step by step.
- `opes.py`: script version of the same workflow. This is the file used for
  production or submitted runs. It accepts the simulation temperature, OPES
  flavor, bias barrier, and input structure as command-line arguments.
- `leonardo.sbatch`: SLURM job script for CINECA Leonardo.

## Output Directories

Each run creates a directory containing the following files:

- `plumed.dat`: generated PLUMED input file. It defines the Fe and N atom
  groups, the collective variables, upper walls, the OPES action, and the
  `PRINT` command.
- `COLVAR`: PLUMED time series containing the collective variables and bias
  terms printed during the simulation.
- `KERNELS`: OPES kernel file. It stores the adaptive bias kernels deposited by
  OPES and is used for analysis or reconstruction of the bias.
- `STATES`: OPES state file written during the simulation. It can be used to
  restart or continue the adaptive bias.
- `ENERGY`: custom MD log written by `opes.py`, with simulation time, potential
  energy, kinetic energy, total energy, instantaneous temperature, and elapsed
  CPU time.
- `traj.traj`: ASE trajectory file with saved atomic configurations.
- `traj.xyz`: XYZ conversion of the trajectory, convenient for visualization in
  external molecular viewers.