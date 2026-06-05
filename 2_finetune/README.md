# Fine-Tuning Workflow

This tutorial extends the first OPES exercise by improving the potential in the
region of configuration space sampled during N2 dissociation on Fe(111).

The workflow is:

1. Select informative configurations from an OPES trajectory with DEAL.
2. Label the selected structures with reference energies and forces.
3. Fine-tune a MACE-based model with Franken.
4. Repeat OPES sampling with the fine-tuned potential and compare with the
   universal-model run.

In the school material, the labeling step uses a larger and more expressive MACE-Multihead model (`mace_mp(model="mh-1")`) as a
stand-in for expensive DFT calculations. In a production workflow this step is
where the selected structures would be sent to the chosen electronic-structure
code.

## Data Flow

```text
../1_opes/700K_explore/traj.xyz.gz
        |
        v
1_deal_selection/max_200/deal_selected.xyz
        |
        v
2_dft_labeling/deal_labeled.xyz
        |
        v
3_franken_finetune/autotune/*/best_ckpt.pt
        |
        v
4_opes_sampling/700K-explore/
```

## Folders

- `1_deal_selection/`: data-efficient selection of representative structures
  from the OPES trajectory.
- `2_dft_labeling/`: reference labeling of selected structures and creation of
  train/validation splits.
- `3_franken_finetune/`: Franken fine-tuning and model-selection analysis.
- `4_opes_sampling/`: OPES simulation using the fine-tuned potential.

Each subfolder has its own README with the files, commands, and generated
outputs for that stage.
