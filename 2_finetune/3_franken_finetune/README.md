# 3. Franken Fine-Tuning

Code and description: https://franken.readthedocs.io/w

This stage fine-tunes a MACE-based model with Franken using the labeled
structures from `../2_dft_labeling/`. The goal is to improve the potential in the
N2/Fe configurations selected from enhanced sampling, without retraining a model
from scratch.

## Inputs

The Franken batch scripts expect `train.xyz` and `val.xyz` in this folder. Either
copy them from the labeling stage or create symlinks:

```bash
ln -s ../2_dft_labeling/train.xyz train.xyz
ln -s ../2_dft_labeling/val.xyz val.xyz
```

## Files

- `franken.sbatch`: hyperparameter autotuning run for a MACE backbone. It writes
  results under `autotune/`.
- `franken-data.sbatch`: sample-efficiency sweep. It repeats training with
  increasing numbers of selected structures and writes results under
  `sample_efficiency/`.
- `analysis.ipynb`: reads Franken `best.json` files and plots train/validation
  force errors as a function of the number of training structures.

## Running

For hyperparameter search:

```bash
sbatch franken.sbatch
```

For the sample-efficiency exercise:

```bash
sbatch franken-data.sbatch
```

The model checkpoint selected for the next OPES stage is the `best_ckpt.pt`
produced by the chosen Franken run. Copy or symlink that checkpoint into
`../4_opes_sampling/`, or edit the OPES submission script to point to its
location.
