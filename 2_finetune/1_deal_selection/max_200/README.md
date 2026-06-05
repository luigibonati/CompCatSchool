# DEAL Selection: 

This folder contains the prepared DEAL selection example used in the tutorial.
It selects up to 200 configurations from the OPES trajectory generated with the
universal MACE model.

## Files

- `deal.yaml`: selection configuration. The trajectory source is the simulation done in the previous step.
- `submit.sbatch`: HPC submission script for running DEAL.
- `deal_selected.xyz`: selected structures. This is the file consumed by the
  labeling step.
- `chemiscope.ipynb`: visualization notebook for checking selected structures.
