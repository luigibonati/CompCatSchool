# 1. DEAL Selection

Code and description: https://github.com/luigibonati/DEAL 

This stage selects a compact, informative subset of configurations from the
baseline OPES trajectory. The aim is to avoid labeling every MD frame while still
covering the parts of configuration space that matter for fine-tuning.

DEAL reads the OPES trajectory, builds an uncertainty/diversity criterion, and
incrementally selects structures for the reference-labeling step.

## Contents

- `max_200/`: concrete selection run used in the tutorial. It is configured to
  select up to 200 structures.

Inside `max_200/`:

- `deal.yaml`: DEAL configuration. It points to
  `../../../1_opes/700K_explore/traj.xyz.gz` and sets the selection parameters.
- `submit.sbatch`: Leonardo batch script for running DEAL.
- `deal_selected.xyz`: selected configurations passed to the labeling step.
- `chemiscope.ipynb`: inspect selected structures and
  uncertainty/CV information.

## Typical Use

```bash
cd 2_finetune/1_deal_selection/max_200
deal -c deal.yaml --max 200
```

On Leonardo, use the batch script after checking that the environment and input
trajectory path match the current machine:

```bash
sbatch submit.sbatch
```

The output needed by the next stage is `max_200/deal_selected.xyz`.
