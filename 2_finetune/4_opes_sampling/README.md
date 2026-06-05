# 4. OPES Sampling with the Fine-Tuned Potential

This final stage repeats the OPES enhanced-sampling calculation using the
fine-tuned Franken/MACE potential. The purpose is to compare how the improved
model changes the sampled configurations and the OPES outputs relative to the
baseline universal MACE run in `../../1_opes/`.

## Files

- `opes.sbatch`: Leonardo job script for running OPES with a Franken checkpoint.
  It calls `../1_opes/opes.py` with the `--franken` option.
- `700K-explore/`: example OPES output directory from a 700 K exploratory run.
- `slurm-*.out`: scheduler logs from submitted OPES runs.

The OPES output directory contains the same file types as the baseline OPES
exercise:

- `plumed.dat`: generated PLUMED input.
- `COLVAR`: collective variables and bias terms.
- `KERNELS`: OPES adaptive-bias kernels.
- `STATES` and `bck.last.STATES`: OPES state and backup files.
- `ENERGY`: MD energy and temperature log.
- `traj.xyz.gz`: compressed trajectory for visualization or later analysis.

## Running

Place the selected Franken checkpoint in this folder as `best_ckpt.pt`, or edit
the `--franken` path in `opes.sbatch`. Also check the relative paths to
`opes.py` and `init_config.xyz` before submitting, since they depend on the
directory from which the job is launched. Then submit:

```bash
sbatch opes.sbatch
```

The provided script launches a 700 K `OPES_METAD_EXPLORE` run using
`../../0_system/init_config.xyz` as the starting structure.

## What to Compare

After the run, compare the fine-tuned-potential output with the baseline OPES
run:

- trajectories: does the fine-tuned model visit the same N2/Fe configurations?
- `COLVAR`: are `d_N2` and `c_N_Fe` sampled similarly?
- `ENERGY`: are the dynamics stable and temperatures controlled?
- `KERNELS`/`STATES`: did OPES build a comparable adaptive bias?
