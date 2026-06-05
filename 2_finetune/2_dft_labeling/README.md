# 2. Reference Labeling

This stage assigns reference energies and forces to the selected configurations.
In a real fine-tuning workflow these labels would usually come from DFT. For the
tutorial, `label_structures.py` uses a higher-level pretrained MACE model
(`mace_mp(model="mh-1")`) as a fast stand-in for DFT so the full workflow can be
demonstrated without launching electronic-structure calculations.

## Files

- `label_structures.py`: reads selected configurations, evaluates reference
  energies and forces, and writes labeled datasets.
- `deal_labeled.xyz`: selected structures after assigning reference energy and
  force labels.
- `train.xyz`: training split used by Franken.
- `val.xyz`: validation split used for model selection.

## Running

Check the input path in `label_structures.py` before running. The prepared
selection in this repository is:

```text
../1_deal_selection/max_200/deal_selected.xyz
```

Then run:

```bash
python label_structures.py
```

The script writes a 160-structure training set and the remaining  for validation. These two files are the inputs for
`../3_franken_finetune/`.